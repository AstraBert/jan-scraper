from transformers import (
    BartForConditionalGeneration,
    BigBirdPegasusForConditionalGeneration,
    BlenderbotForConditionalGeneration,
    BlenderbotSmallForConditionalGeneration,
    EncoderDecoderModel,
    FSMTForConditionalGeneration,
    GPTSanJapaneseForConditionalGeneration,
    LEDForConditionalGeneration,
    LongT5ForConditionalGeneration,
    M2M100ForConditionalGeneration,
    MarianMTModel,
    MBartForConditionalGeneration,
    MT5ForConditionalGeneration,
    MvpForConditionalGeneration,
    NllbMoeForConditionalGeneration,
    PegasusForConditionalGeneration,
    PegasusXForConditionalGeneration,
    PLBartForConditionalGeneration,
    ProphetNetForConditionalGeneration,
    SwitchTransformersForConditionalGeneration,
    T5ForConditionalGeneration,
    XLMProphetNetForConditionalGeneration,
    BartForCausalLM,
    BertLMHeadModel,
    BertGenerationDecoder,
    BigBirdForCausalLM,
    BigBirdPegasusForCausalLM,
    BioGptForCausalLM,
    BlenderbotForCausalLM,
    BlenderbotSmallForCausalLM,
    BloomForCausalLM,
    CamembertForCausalLM,
    LlamaForCausalLM,
    CodeGenForCausalLM,
    CpmAntForCausalLM,
    CTRLLMHeadModel,
    Data2VecTextForCausalLM,
    ElectraForCausalLM,
    ErnieForCausalLM,
    GitForCausalLM,
    GPT2LMHeadModel,
    GPTBigCodeForCausalLM,
    GPTNeoForCausalLM,
    GPTNeoXForCausalLM,
    GPTNeoXJapaneseForCausalLM,
    GPTJForCausalLM,
    LlamaForCausalLM,
    MarianForCausalLM,
    MBartForCausalLM,
    MegaForCausalLM,
    MegatronBertForCausalLM,
    MvpForCausalLM,
    OpenLlamaForCausalLM,
    OpenAIGPTLMHeadModel,
    OPTForCausalLM,
    PegasusForCausalLM,
    PLBartForCausalLM,
    ProphetNetForCausalLM,
    QDQBertLMHeadModel,
    ReformerModelWithLMHead,
    RemBertForCausalLM,
    RobertaForCausalLM,
    RobertaPreLayerNormForCausalLM,
    RoCBertForCausalLM,
    RoFormerForCausalLM,
    RwkvForCausalLM,
    Speech2Text2ForCausalLM,
    TransfoXLLMHeadModel,
    TrOCRForCausalLM,
    XGLMForCausalLM,
    XLMWithLMHeadModel,
    XLMProphetNetForCausalLM,
    XLMRobertaForCausalLM,
    XLMRobertaXLForCausalLM,
    XLNetLMHeadModel,
    XmodForCausalLM,
)

CAUSAL_HF_MODELS = {
    "bart": BartForCausalLM,
    "bert": BertLMHeadModel,
    "bert-generation": BertGenerationDecoder,
    "big_bird": BigBirdForCausalLM,
    "bigbird_pegasus": BigBirdPegasusForCausalLM,
    "biogpt": BioGptForCausalLM,
    "blenderbot": BlenderbotForCausalLM,
    "blenderbot-small": BlenderbotSmallForCausalLM,
    "bloom": BloomForCausalLM,
    "camembert": CamembertForCausalLM,
    "code_llama": LlamaForCausalLM,
    "codegen": CodeGenForCausalLM,
    "cpmant": CpmAntForCausalLM,
    "ctrl": CTRLLMHeadModel,
    "data2vec-text": Data2VecTextForCausalLM,
    "electra": ElectraForCausalLM,
    "ernie": ErnieForCausalLM,
    "git": GitForCausalLM,
    "gpt-sw3": GPT2LMHeadModel,
    "gpt2": GPT2LMHeadModel,
    "gpt_bigcode": GPTBigCodeForCausalLM,
    "gpt_neo": GPTNeoForCausalLM,
    "gpt_neox": GPTNeoXForCausalLM,
    "gpt_neox_japanese": GPTNeoXJapaneseForCausalLM,
    "gptj": GPTJForCausalLM,
    "llama": LlamaForCausalLM,
    "marian": MarianForCausalLM,
    "mbart": MBartForCausalLM,
    "mega": MegaForCausalLM,
    "megatron-bert": MegatronBertForCausalLM,
    "mvp": MvpForCausalLM,
    "open-llama": OpenLlamaForCausalLM,
    "openai-gpt": OpenAIGPTLMHeadModel,
    "opt": OPTForCausalLM,
    "pegasus": PegasusForCausalLM,
    "plbart": PLBartForCausalLM,
    "prophetnet": ProphetNetForCausalLM,
    "qdqbert": QDQBertLMHeadModel,
    "reformer": ReformerModelWithLMHead,
    "rembert": RemBertForCausalLM,
    "roberta": RobertaForCausalLM,
    "roberta-prelayernorm": RobertaPreLayerNormForCausalLM,
    "roc_bert": RoCBertForCausalLM,
    "roformer": RoFormerForCausalLM,
    "rwkv": RwkvForCausalLM,
    "speech_to_text_2": Speech2Text2ForCausalLM,
    "transfo-xl": TransfoXLLMHeadModel,
    "trocr": TrOCRForCausalLM,
    "xglm": XGLMForCausalLM,
    "xlm": XLMWithLMHeadModel,
    "xlm-prophetnet": XLMProphetNetForCausalLM,
    "xlm-roberta": XLMRobertaForCausalLM,
    "xlm-roberta-xl": XLMRobertaXLForCausalLM,
    "xlnet": XLNetLMHeadModel,
    "xmod": XmodForCausalLM,
}

SEQ2SEQ_HF_MODELS = {
    "bart": BartForConditionalGeneration,
    "bigbird_pegasus": BigBirdPegasusForConditionalGeneration,
    "blenderbot": BlenderbotForConditionalGeneration,
    "blenderbot-small": BlenderbotSmallForConditionalGeneration,
    "encoder-decoder": EncoderDecoderModel,
    "fsmt": FSMTForConditionalGeneration,
    "gptsan-japanese": GPTSanJapaneseForConditionalGeneration,
    "led": LEDForConditionalGeneration,
    "longt5": LongT5ForConditionalGeneration,
    "m2m_100": M2M100ForConditionalGeneration,
    "marian": MarianMTModel,
    "mbart": MBartForConditionalGeneration,
    "mt5": MT5ForConditionalGeneration,
    "mvp": MvpForConditionalGeneration,
    "nllb-moe": NllbMoeForConditionalGeneration,
    "pegasus": PegasusForConditionalGeneration,
    "pegasus_x": PegasusXForConditionalGeneration,
    "plbart": PLBartForConditionalGeneration,
    "prophetnet": ProphetNetForConditionalGeneration,
    "switch_transformers": SwitchTransformersForConditionalGeneration,
    "t5": T5ForConditionalGeneration,
    "xlm-prophetnet": XLMProphetNetForConditionalGeneration,
}


def longest_in_list(l):
    """
    Finds and returns the longest element in a list.

    Args:
        l (list): List of elements.

    Returns:
        Any: The longest element in the list.
    """
    lens = [len(i) for i in l]
    maxind = lens.index(max(lens))
    return l[maxind]


def choose_right_model(model_name, model_task):
    """
    Chooses the right Hugging Face model based on the provided model name and task.

    Args:
        model_name (str): Name or identifier of the Hugging Face model.
        model_task (str): Task associated with the model.

    Returns:
        str: The chosen Hugging Face model.

    Raises:
        Exception: Raised if the model is not supported.
    """
    model_split = model_name.split("/")
    if len(model_split) > 0:
        model_split_name = model_split[len(model_split) - 1]
    else:
        model_split_name = model_split[0]
    if model_task == "text2text-generation":
        keys_in_name = []
        for key in SEQ2SEQ_HF_MODELS:
            if key in model_split_name:
                keys_in_name.append(key)
        if len(keys_in_name) == 0:
            raise Exception("Model not supported")
        if len(keys_in_name) == 1:
            return SEQ2SEQ_HF_MODELS[keys_in_name[0]]
        else:
            return SEQ2SEQ_HF_MODELS[longest_in_list(keys_in_name)]
    if model_task == "text-generation":
        keys_in_name = []
        for key in CAUSAL_HF_MODELS:
            if key in model_split_name:
                keys_in_name.append(key)
        if len(keys_in_name) == 0:
            raise Exception("Model not supported")
        if len(keys_in_name) == 1:
            return CAUSAL_HF_MODELS[keys_in_name[0]]
        else:
            return CAUSAL_HF_MODELS[longest_in_list(keys_in_name)]


def supported_causalLM_models():
    """
    Prints a list of supported causal language models.
    """
    print(list(CAUSAL_HF_MODELS.keys()))


def supported_seq2seqLM_models():
    """
    Prints a list of supported sequence-to-sequence language models.
    """
    print(list(SEQ2SEQ_HF_MODELS.keys()))
