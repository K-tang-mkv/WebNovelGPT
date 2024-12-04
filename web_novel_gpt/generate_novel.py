import re
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from web_novel_gpt.config import WebNovelGenerationConfig
from web_novel_gpt.cost import Cost
from web_novel_gpt.llm import LLM
from web_novel_gpt.logger import logger
from web_novel_gpt.prompts.chapter_outline_generator_prompt import (
    CHAPTER_OUTLINE_GENERATOR_PROMPT,
)
from web_novel_gpt.prompts.content_generator_prompt import CONTENT_GENERATOR_PROMPT
from web_novel_gpt.prompts.content_optimizer_prompt import CONTENT_OPTIMIZER_PROMPT
from web_novel_gpt.prompts.detail_outline_generator_prompt import (
    DETAILED_OUTLINE_GENERATOR_PROMPT_V2,
    DETAILED_OUTLINE_SUMMARY_PROMPT,
)
from web_novel_gpt.prompts.intent_analyzer_prompt import INTENT_ANALYZER_PROMPT
from web_novel_gpt.prompts.rough_outline_prompt import ROUGH_OUTLINE_GENERATOR_PROMPT_V2
from web_novel_gpt.schema import (
    Chapter,
    ChapterOutline,
    CheckpointType,
    DetailedOutline,
    Novel,
    NovelIntent,
    NovelSaver,
    NovelVolume,
    OutlineType,
    RoughOutline,
)
from web_novel_gpt.utils import extract_outline, parse_intent, save_checkpoint


class WebNovelGPT(BaseModel):
    """Web novel generation main class."""

    llm: LLM = Field(default_factory=LLM)
    cost_tracker: Cost = Field(default_factory=Cost)
    novel_saver: NovelSaver = Field(default_factory=NovelSaver)
    generation_config: WebNovelGenerationConfig = Field(
        default_factory=WebNovelGenerationConfig
    )

    novel_id: Optional[str] = Field(None, exclude=True)
    intent: Optional[NovelIntent] = Field(None, exclude=True)

    current_volumes: List[NovelVolume] = Field(default_factory=list, exclude=True)
    current_rough_outline: Optional[RoughOutline] = Field(None, exclude=True)
    current_chapter_outline: Optional[ChapterOutline] = Field(None, exclude=True)
    current_detailed_outline: Optional[DetailedOutline] = Field(None, exclude=True)

    current_volume_num: Optional[int] = Field(None, exclude=True)
    current_chapter_num: Optional[int] = Field(None, exclude=True)

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def generate_novel_id(description: str) -> str:
        """Generate unique novel ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{description[:5]}_{timestamp}"

    async def analyze_intent(self, user_input: str) -> NovelIntent:
        """Analyze user input to extract story details."""
        logger.info("Analyzing user input to extract story details")
        prompt = INTENT_ANALYZER_PROMPT.format(user_input=user_input)
        response = await self.llm.ask(prompt)
        title, description, genre = parse_intent(response)
        return NovelIntent(
            title=title,
            description=description,
            genre=genre,
        )

    async def generate_rough_outline(self, user_input: str) -> RoughOutline:
        """Generate rough outline based on story intent."""
        logger.info(f"Generating rough outline for novel '{self.intent.title}'")
        prompt = ROUGH_OUTLINE_GENERATOR_PROMPT_V2.format(
            user_input=user_input,
            title=self.intent.title,
            genre=self.intent.genre,
            description=self.intent.description,
            volume_count=self.generation_config.volume_count,
        )
        response = await self.llm.ask(prompt)
        return extract_outline(response, OutlineType.ROUGH)

    async def generate_detailed_outline(
        self, prev_volume_summary: Optional[str] = None
    ) -> DetailedOutline:
        """Generate detailed outline for a single chapter."""
        # FIXME: rough_outline should be fix
        prompt = DETAILED_OUTLINE_GENERATOR_PROMPT_V2.format(
            designated_volume=self.current_volume_num,
            designated_chapter=self.current_chapter_num,
            description=self.intent.description,
            rough_outline=str(self.current_rough_outline),
            section_word_count=self.generation_config.section_word_count,
            prev_volume_summary=prev_volume_summary,
            chapter_outline=self.current_chapter_outline,
        )
        response = await self.llm.ask(prompt)
        return extract_outline(response, OutlineType.DETAILED)

    @save_checkpoint(CheckpointType.CHAPTER)
    async def generate_chapter(self, existing_chapters: List[Chapter]) -> Chapter:
        """Generate a single chapter."""
        chapters = [
            f"{chapter.title}\n{chapter.content}" for chapter in existing_chapters
        ]
        prompt = CONTENT_GENERATOR_PROMPT.format(
            designated_chapter=self.current_chapter_num,
            rough_outline=str(self.current_rough_outline),
            detailed_outline=self.current_detailed_outline,
            section_word_count=self.generation_config.section_word_count,
            chapters="\n\n".join(chapters),
        )
        response = await self.llm.ask(prompt)
        # Extract chapter title and content
        title = re.search(r"## 第[0-9]+章 .+", response).group()
        content = response.replace(title, "").strip()
        return Chapter(title=title, content=content)

    @save_checkpoint(CheckpointType.CHAPTER)
    async def _optimize_chapter(self, chapter: str) -> str:
        """Optimize a single chapter."""
        prompt = CONTENT_OPTIMIZER_PROMPT.format(
            chapter_content=chapter,
            section_word_count=self.generation_config.section_word_count,
        )
        return await self.llm.ask(prompt)

    async def generate_chapter_outline(
        self, prev_volume_summary: Optional[str] = None
    ) -> ChapterOutline:
        """Generate chapter outline for a volume."""
        prompt = CHAPTER_OUTLINE_GENERATOR_PROMPT.format(
            designated_volume=self.current_volume_num,
            designated_chapter=self.current_chapter_num,
            description=self.intent.description,
            rough_outline=str(self.current_rough_outline),
            section_word_count=self.generation_config.section_word_count,
            prev_volume_summary=prev_volume_summary,
        )
        response = await self.llm.ask(prompt)
        return extract_outline(response, OutlineType.CHAPTER)

    @save_checkpoint(CheckpointType.VOLUME)
    async def generate_volume(
        self,
        prev_volume_summary: Optional[str] = None,
    ) -> NovelVolume:
        """Generate a complete volume of the novel."""
        logger.info(f"Starting generation of volume {self.current_volume_num}")

        # Initialize volume with empty data first
        volume = NovelVolume(volume_num=self.current_volume_num)

        # Generate chapters one by one
        chapter_count_per_volume = self.generation_config.chapter_count_per_volume
        start_chapter = chapter_count_per_volume * (self.current_volume_num - 1) + 1
        end_chapter = self.current_volume_num * chapter_count_per_volume
        for chapter_num in range(start_chapter, end_chapter):
            self.current_chapter_num = chapter_num + 1
            await self._generate_single_chapter(
                volume=volume, prev_volume_summary=prev_volume_summary
            )
            logger.info(
                f"Successfully generated chapter {chapter_num + 1} in volume {self.current_volume_num}"
            )

        return volume

    async def _generate_single_chapter(
        self,
        volume: NovelVolume,
        prev_volume_summary: Optional[str],
    ) -> None:
        """Generate a single chapter including its outlines and content."""
        # Generate chapter outline for current chapter
        self.current_chapter_outline = await self.generate_chapter_outline(
            prev_volume_summary=prev_volume_summary
        )
        volume.chapter_outline = self.current_chapter_outline

        # Generate detailed outline for current chapter
        self.current_detailed_outline = await self.generate_detailed_outline(
            prev_volume_summary=prev_volume_summary
        )
        volume.detailed_outline = self.current_detailed_outline

        # Generate current chapter
        chapter = await self.generate_chapter(volume.chapters)
        volume.chapters.append(chapter)

    async def generate_volumes(self) -> List[NovelVolume]:
        """Generate volumes for the novel."""
        volumes: List[NovelVolume] = []

        for volume_num in range(self.generation_config.volume_count):
            self.current_volume_num = volume_num + 1
            volume = await self.generate_volume()
            volumes.append(volume)

        return volumes

    @save_checkpoint(CheckpointType.NOVEL)
    async def generate_novel(
        self,
        user_input: str,
        genre: Optional[str] = None,
        resume_novel_id: Optional[str] = None,
    ) -> Novel:
        """Generate complete novel from user input."""
        # Resume from checkpoint if provided
        if resume_novel_id:
            self.novel_id = resume_novel_id
            return await self._resume_generation()

        logger.info("Starting new novel generation")
        self.intent = await self.analyze_intent(user_input)
        if genre:
            self.intent.genre = genre

        self.novel_id = self.generate_novel_id(self.intent.description)
        self.current_rough_outline = await self.generate_rough_outline(user_input)

        self.current_volumes = await self.generate_volumes()

        novel = Novel(
            intent=self.intent,
            rough_outline=self.current_rough_outline,
            volumes=self.current_volumes,
            cost_info=self.cost_tracker.get(),
        )

        return novel

    @save_checkpoint(CheckpointType.NOVEL)
    async def _resume_generation(self) -> Novel:
        """从检查点恢复小说生成"""

    async def generate_detailed_outline_summary(
        self,
        volume_num: int,
        rough_outline: str,
        detailed_outline: str,
    ) -> str:
        """Generate summary of detailed outline."""
        prompt = DETAILED_OUTLINE_SUMMARY_PROMPT.format(
            volume_num=volume_num,
            rough_outline=rough_outline,
            detailed_outline=detailed_outline,
        )
        return await self.llm.ask(prompt)
