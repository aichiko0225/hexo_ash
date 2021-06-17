FROM node:latest
FROM nginx:latest

RUN npm install -g npm
RUN rm -rf node_modules
RUN npm install

RUN hexo clean
RUN hexo generate

# 运行命令
CMD ["nginx", "-g", "daemon off;"]