FROM node:latest

RUN rm -rf node_modules
RUN npm install

RUN hexo clean
RUN hexo generate

# 运行命令
CMD ["node"]