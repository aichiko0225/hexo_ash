FROM node:latest

COPY package*.json ./

# RUN npm install -g npm
RUN rm -rf node_modules

# 安装hexo脚手架
RUN yarn global add hexo-cli

RUN yarn install

# RUN hexo clean
# RUN hexo generate
ENTRYPOINT ["hexo", "clean"]

CMD ["hexo", "generate"]

WORKDIR /www/hexo_ash

COPY . .

FROM nginx:latest

# 运行命令
CMD ["nginx", "-g", "daemon off;"]