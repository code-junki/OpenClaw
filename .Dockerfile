# Source: https://github.com/ROCm/AAI-2026-Workshops-Dev/blob/main/Workshop%2001%20-%20Openclaw/Dockerfile
# Build command: docker build -t edaamd/openclaw-cpp-aai-no-modelnet-7-1:latest .
FROM rocm/dev-ubuntu-24.04:7.2.1-complete

ENV DEBIAN_FRONTEND=noninteractive

# Install Node.js 24.x and build dependencies
RUN apt-get update && \
    apt-get install -y \
        curl \
        git \
        cmake \
        build-essential \
        python3-pip \
        ca-certificates \
        libssl-dev && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# git-wrapper: transparently route `git clone` of GitHub repos through
# gh-proxy.org (with a plain http://github.com fallback), same pattern as
# jupyter-base/Dockerfile.git-proxy-test. Installed to /usr/local/bin so it
# shadows the real /usr/bin/git for both the build below and interactive use.
COPY git-wrapper /usr/local/bin/git
RUN chmod +x /usr/local/bin/git && /usr/local/bin/git --version

# Install openclaw globally
RUN npm install -g openclaw@2026.7.1

# Install Jupyter and huggingface-hub
RUN pip3 install --break-system-packages jupyter huggingface-hub ihighlight

# Build llama.cpp with ROCm support
WORKDIR /workspace
RUN git clone https://github.com/ggml-org/llama.cpp.git && \
    cd llama.cpp && \
    mkdir build && \
    cd build && \
    cmake .. -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx1100 -DLLAMA_CURL=ON && \
    cmake --build . --config Release -j$(nproc)

# Create cache directory and download model (Q6_K for high quality + vision support)
# RUN mkdir -p /workspace/hf_cache && \
#     hf download unsloth/Qwen3.6-35B-A3B-GGUF --include "*Q6_K.gguf" --include "mmproj-BF16.gguf"

# Set runtime paths (adjust WORKSPACE_DIR based on mounting in Radeon Cloud)
ENV WORKSPACE_DIR=/workspace/openclaw-cpp-aai-latest
ENV HF_HOME=${WORKSPACE_DIR}/hf_cache
ENV PATH=${WORKSPACE_DIR}/llama.cpp/build/bin:$PATH
ENV LD_LIBRARY_PATH=${WORKSPACE_DIR}/llama.cpp/build/bin:${WORKSPACE_DIR}/llama.cpp/build

# Create startup script with llama-server auto-configuration
RUN cat > /usr/local/bin/docker-entrypoint.sh << 'EOF'
#!/bin/bash

# Auto-configure llama-server path
if [ -z "$LLAMA_CONFIGURED" ]; then
  LLAMA_BIN=$(find /workspace -name 'llama-server' -type f 2>/dev/null | head -1 | xargs dirname)
  if [ -n "$LLAMA_BIN" ]; then
    export PATH="$LLAMA_BIN:$PATH"
    LLAMA_BUILD=$(dirname "$LLAMA_BIN")
    export LD_LIBRARY_PATH="$LLAMA_BIN:$LLAMA_BUILD:$LD_LIBRARY_PATH"
    export WORKSPACE_DIR=$(echo $LLAMA_BIN | cut -d'/' -f1-3)
    export HF_HOME="/models"
    export LLAMA_CONFIGURED=1
  fi
fi

# Execute the command passed to docker run, or start bash if none
exec "${@:-/bin/bash}"
EOF

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Use the startup script as entrypoint
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
