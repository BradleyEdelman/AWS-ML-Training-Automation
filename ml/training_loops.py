import tensorflow as tf
from transformers import Trainer, TrainingArguments
import yaml
from ml import checkpoint_save

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

EPOCHS = config["training"]["epochs"]
CHECKPOINT_INTERVAL = config["training"]["checkpoint_interval"]
CHECKPOINT_DIR = config["training"]["checkpoint_dir"]


def train_cnn(model, dataset):

    for epoch in range(1, EPOCHS + 1):
        print(f"Training CNN Epoch {epoch}/{EPOCHS}")
        model.fit(dataset, epochs=1)

        # Manually save checkpoint every X epochs
        if epoch % CHECKPOINT_INTERVAL == 0:
            checkpoint_save.save_checkpoint(model, epoch=epoch)

    checkpoint_save.save_checkpoint(model, epoch="final")


def train_gpt2(model, dataset):
    """
    Fine-tunes GPT-2 using Hugging Face Trainer with **manual** epoch-by-epoch checkpointing.
    """
    training_args = TrainingArguments(
        output_dir=CHECKPOINT_DIR,
        save_strategy="no",  # disable auto_checkpointing, we do it ourselves
        num_train_epochs=EPOCHS,  # Train one epoch at a time
        per_device_train_batch_size=2,
    )

    trainer = Trainer(model=model, args=training_args, train_dataset=dataset)

    for epoch in range(1, EPOCHS + 1):
        print(f"Fine-tuning GPT-2 - Epoch {epoch}/{EPOCHS}")
        trainer.train(resume_from_checkpoint=True)  # Train one epoch at a time

        # Manually save checkpoint every X epochs
        if epoch % CHECKPOINT_INTERVAL == 0:
            checkpoint_save.save_checkpoint(model, epoch=epoch)

    # Final checkpoint save
    checkpoint_save.save_checkpoint(model, epoch="final")


def train_dcgan(model, dataset):
    """
    Training loop for GANs with manual checkpointing every X epochs.
    """
    generator = model["generator"]
    discriminator = model["discriminator"]

    for epoch in range(1, EPOCHS + 1):
        print(f"Training GAN Epoch {epoch}/{EPOCHS}")

        for real_images in dataset:
            noise = tf.random.normal([real_images.shape[0], 100])
            generated_images = generator(noise, training=True)
            real_output = discriminator(real_images, training=True)
            fake_output = discriminator(generated_images, training=True)

        # Manually save checkpoint every X epochs
        if epoch % CHECKPOINT_INTERVAL == 0:
            checkpoint_save.save_checkpoint(model, epoch=epoch)

    # Final checkpoint save
    checkpoint_save.save_checkpoint(model, epoch="final")

