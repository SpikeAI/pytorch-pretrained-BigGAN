import torch
from pytorch_pretrained_biggan import (BigGAN, one_hot_from_names, truncated_noise_sample,
                                       save_as_images, display_in_terminal)

# OPTIONAL: if you want to have more information on what's happening, activate the logger as follows
import logging
logging.basicConfig(level=logging.INFO)

# Load pre-trained model tokenizer (vocabulary)
model = BigGAN.from_pretrained('biggan-deep-256')

# Prepare a input
truncation = 0.4
class_vector = one_hot_from_names(['soap bubble', 'coffee', 'mushroom'], batch_size=3)
noise_vector = truncated_noise_sample(truncation=truncation, batch_size=3)

# All in tensors
noise_vector = torch.from_numpy(noise_vector)
class_vector = torch.from_numpy(class_vector)

if torch.cuda.is_available():
    # If you have a GPU, put everything on cuda
    noise_vector = noise_vector.to('cuda')
    class_vector = class_vector.to('cuda')
    model.to('cuda')

# Generate an image
with torch.no_grad():
    output = model(noise_vector, class_vector, truncation)

if torch.cuda.is_available():
    # If you have a GPU put back on CPU
    output = output.to('cpu')

try:
    # If you have a sixtel compatible terminal you can display the images in the terminal
    # (see https://github.com/saitoha/libsixel for details)
    display_in_terminal(output)
except:
    pass

try:
    # Save results as png images
    save_as_images(output)
except:
    pass
