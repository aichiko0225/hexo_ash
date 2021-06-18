FROM nginx:latest

ADD ./conf/nginx.conf /etc/nginx/nginx.conf

# 运行命令
CMD ["nginx", "-g", "daemon off;"]