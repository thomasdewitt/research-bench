# Start from Claude Code devcontainer base
FROM node:20

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    zsh \
    sudo \
    iptables \
    ipset \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Miniforge
RUN curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh" \
    && bash Miniforge3-$(uname)-$(uname -m).sh -b -p /opt/miniforge3 \
    && rm Miniforge3-$(uname)-$(uname -m).sh

ENV PATH="/opt/miniforge3/bin:$PATH"

# Create and configure main environment with required packages
RUN conda create -n main python=3.10 -y && \
    /opt/miniforge3/envs/main/bin/pip install \
    numpy \
    pandas \
    matplotlib \
    scipy \
    objscale \
    scaleinvariance

# Set up non-root user
ARG USERNAME=node
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME || true \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/zsh || true \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install Claude Code CLI
RUN npm install -g @anthropic-ai/claude-code

# Copy and set up firewall script (from claude-code devcontainer)
COPY init-firewall.sh /usr/local/bin/init-firewall.sh
RUN chmod +x /usr/local/bin/init-firewall.sh

USER $USERNAME
WORKDIR /workspace

# Activate conda environment by default
RUN echo "source /opt/miniforge3/etc/profile.d/conda.sh && conda activate main" >> ~/.zshrc
ENV PATH="/opt/miniforge3/envs/main/bin:$PATH"

ENTRYPOINT ["/bin/zsh", "-c", "sudo /usr/local/bin/init-firewall.sh && exec \"$@\"", "--"]
