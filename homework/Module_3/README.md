## Building a voice agent

An exciting assignment on building a voice agents.

We start by building the interface, which uses the Fast API library to create `post` API endpoint `/chat/` that accepts an audio file

You can use [Postman](https://www.postman.com/downloads/) to test this out.

---

### Running the project locally

To run the project locally we need to start a server using `uvicorn`

``` bash
uvicorn main:app --reload
```

---

### Transcription

I transcribed my audio using the [openai-whisper](https://github.com/openai/whisper?tab=readme-ov-file) library

---

### LLM

Using huggingface [Transformers](https://huggingface.co/docs/transformers/en/installation) library


### Dependencies

Found in the `requirements.txt` file.