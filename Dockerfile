# FROM node:latest

# RUN mkdir /app

# COPY . /app/

# WORKDIR /app

# RUN npm install hexo-cli -g
# RUN rm -rf node_modules && yarn install

# RUN hexo clean && hexo generate

# COPY . /app/

# CMD ["npm", "run-script"]

FROM nginx:latest

# WORKDIR /app

# COPY ./public /usr/share/nginx/html
ADD ./conf/nginx.conf /etc/nginx/nginx.conf

# 运行命令
CMD ["nginx", "-g", "daemon off;"]