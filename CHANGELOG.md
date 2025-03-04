## [v0.1.0] - 2025.03.04
### Initial pre-release (CNN fine-tuning and checkpointing)
- Automated Spot Instance Training Workflow
    - Launches and configures Spot Instance
    - Transfers training scripts, datasets, and installs dependencies
- Fine-Tune CNN Training with checkpointing
    - Saves model weights at specified interval 
    - Automatically uploads checkpoints to an S3 bucket
- Spot Instance termination handling
    - Detects AWS Spot Instance termination
    - Saves checkpoint before shutdown to prevent progress loss