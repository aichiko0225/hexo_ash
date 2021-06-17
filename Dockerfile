FROM alpine:3.11
FROM node:latest

COPY package*.json ./

# RUN npm install -g npm
RUN rm -rf node_modules

# 安装hexo脚手架
RUN yarn global add hexo-cli

RUN yarn install

COPY . .

# RUN hexo clean
# RUN hexo generate
ENTRYPOINT ["hexo", "clean"]

CMD ["hexo", "generate"]

FROM nginx:latest



# 运行命令
CMD ["nginx", "-g", "daemon off;"]