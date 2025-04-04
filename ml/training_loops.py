import yaml  # type: ignore
from transformers import Trainer, TrainingArguments

from ml import checkpoint_save

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

EPOCHS = config["training"]["epochs"]
CHECKPOINT_INTERVAL = config["training"]["checkpoint_interval"]
CHECKPOINT_DIR = config["training"]["checkpoint_dir"]
MODEL_NAME = config["training"]["model"]


def train_cnn(model, dataset):

    for epoch in range(1, EPOCHS + 1):
        print(f"Training {MODEL_NAME} Epoch {epoch}/{EPOCHS}")
        model.fit(dataset, epochs=1)

        # Manually save checkpoint every X epochs
        if epoch % CHECKPOINT_INTERVAL == 0:
            checkpoint_save.save_checkpoint(model, epoch=epoch)

    checkpoint_save.checkpoint_save(model, epoch="final")


def train_llm(model, tokenizer, dataset):

    with open("config_llm.yaml", "r") as f:
        config_llm = yaml.safe_load(f)

    BATCH_SIZE = config_llm["batch_size"]
    GRAD_ACCUM = config_llm["gradient_accumulation_steps"]
    FP16 = config_llm["use_fp16"]

    training_args = TrainingArguments(
        output_dir=CHECKPOINT_DIR,
        save_strategy="no",  # We do it ourselves
        num_train_epochs=EPOCHS,  # Train one epoch at a time
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRAD_ACCUM,
        fp16=FP16,
    )

    # Need to set padding at least for GPT-2, GPT-J
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    trainer = Trainer(
        model=model, args=training_args, train_dataset=dataset, tokenizer=tokenizer
    )

    for epoch in range(1, EPOCHS + 1):
        print(f"Fine-tuning {MODEL_NAME} - Epoch {epoch}/{EPOCHS}")
        trainer.train()  # Train one epoch at a time

        # Manually save checkpoint every X epochs
        if epoch % CHECKPOINT_INTERVAL == 0:
            checkpoint_save.checkpoint_save(model, epoch=epoch)

    # Final checkpoint save
    checkpoint_save.checkpoint_save(model, epoch="final")


def train_dcgan(model, dataset):

    # generator = model["generator"]
    # discriminator = model["discriminator"]

    for epoch in range(1, EPOCHS + 1):
        print(f"Training GAN Epoch {epoch}/{EPOCHS}")

        # for real_images in dataset:
        #     noise = tf.random.normal([real_images.shape[0], 100])
        #     generated_images = generator(noise, training=True)
        #     real_output = discriminator(real_images, training=True)
        #     fake_output = discriminator(generated_images, training=True)

        # Manually save checkpoint every X epochs
        if epoch % CHECKPOINT_INTERVAL == 0:
            checkpoint_save.checkpoint_save(model, epoch=epoch)

    # Final checkpoint save
    checkpoint_save.checkpoint_save(model, epoch="final")
