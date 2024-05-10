from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from typing import Optional


def local_llm_pipeline(
    model_path: str, kwargs: dict, device: Optional[int] = None
) -> HuggingFacePipeline:
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=64,
        model_kwargs=kwargs,
        device=device,
    )
    return HuggingFacePipeline(pipeline=pipe)
