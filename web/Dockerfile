# --- 第一阶段：编译阶段 ---
# 使用符合 package.json 要求的 Node 22 版本
FROM node:22-alpine AS builder

WORKDIR /app

# 复制依赖文件
COPY package*.json ./

# 安装依赖（如果是在国内服务器，建议加上镜像源）
RUN npm install

# 复制所有源码
COPY . .

# 执行打包（对应你脚本里的 "vite build"）
RUN npm run build

# --- 第二阶段：运行阶段 ---
FROM nginx:latest

# 从 builder 阶段复制 Vite 默认生成的 dist 目录到 nginx 目录
COPY --from=builder /app/dist /usr/share/nginx/html/

# 复制你的 nginx 配置
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]
# FROM nginx:latest

# COPY dist/ /usr/share/nginx/html/
# COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# EXPOSE 80