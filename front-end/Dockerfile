# 参考 https://github.com/vercel/next.js/blob/canary/examples/with-docker-compose/next-app/dev.Dockerfile

FROM node:20-bullseye-slim

WORKDIR /app

# 存在するパッケージマネージャに基づいて依存関係をインストールする
COPY chat/package.json chat/yarn.lock* chat/package-lock.json* chat/pnpm-lock.yaml* ./
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i; \
  # ローカルにNode.jsがインストールされていなくても動作するように，lockfileなしでインストールできるようにする．
  else echo "Warning: Lockfile not found. It is recommended to commit lockfiles to version control." && yarn install; \
  fi

# Next.js collects completely anonymous telemetry data about general usage. Learn more here: https://nextjs.org/telemetry
# Uncomment the following line to disable telemetry at run time
ARG NEXT_TELEMETRY_DISABLED=1
ENV NEXT_TELEMETRY_DISABLED=$NEXT_TELEMETRY_DISABLED

# Note: Don't expose ports here, Compose will handle that for us

ARG NEXT_START_OPTION=
# Start Next.js in development mode based on the preferred package manager
CMD \
  if [ -f yarn.lock ]; then yarn dev ${NEXT_START_OPTION}; \
  elif [ -f package-lock.json ]; then npm run dev ${NEXT_START_OPTION}; \
  elif [ -f pnpm-lock.yaml ]; then pnpm dev ${NEXT_START_OPTION}; \
  else npm run dev ${NEXT_START_OPTION}; \
  fi
