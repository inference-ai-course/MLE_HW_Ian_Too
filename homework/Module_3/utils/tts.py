from indextts.infer_v2 import IndexTTS2

def convert_to_speech(user_text):

    tts = IndexTTS2(cfg_path="/home/iankt/ai-engineer/MLE_HW_Ian_Too/homework/Module_3/index-tts/checkpoints/config.yaml", model_dir="/home/iankt/ai-engineer/MLE_HW_Ian_Too/homework/Module_3/index-tts/checkpoints", use_fp16=False, use_cuda_kernel=False, use_deepspeed=False)
    text = "Translate for me, what is a surprise!"
    tts.infer(spk_audio_prompt='/home/iankt/ai-engineer/MLE_HW_Ian_Too/homework/Module_3/index-tts/checkppoints/examples/voice_01.wav', text=text, output_path="gen.wav", verbose=True)

convert_to_speech("hello")