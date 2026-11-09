FROM node:22-slim AS base

WORKDIR /app

# Install dependencies
FROM base AS deps

COPY package.json package-lock.json ./

RUN npm ci

# Build Next.js application
FROM base AS builder

COPY --from=deps /app/node_modules ./node_modules
COPY . .

ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

RUN npm run build

# Production runtime
FROM base AS runner

ENV NODE_ENV=production
ENV PORT=8080
ENV HOSTNAME=0.0.0.0

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

USER node

EXPOSE 8080

CMD ["node", "server.js"]
