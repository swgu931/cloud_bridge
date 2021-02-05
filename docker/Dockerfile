# Dockerfile written by SW 20210120

FROM ros:foxy-ros-base

SHELL ["/bin/bash", "-c"]

ENV HOSTNAME cloud_bridge

RUN sudo apt-get update -y && sudo apt-get install -y libzmq3-dev apt-utils vim iputils-ping

RUN mkdir /root/src
RUN git clone -b $ROS_DISTRO https://github.com/lge-ros2/cloud_bridge /root/src/cloud_bridge/
WORKDIR /root/src/cloud_bridge
RUN git pull 
WORKDIR /root/src

RUN apt update -y && apt upgrade -y && rosdep update 
RUN rosdep install -y -r -q --from-paths cloud_bridge --ignore-src --rosdistro $ROS_DISTRO
RUN ["/bin/bash", "-c", "source /opt/ros/${ROS_DISTRO}/setup.bash; colcon build --packages-up-to cloud_bridge"]

COPY ./config/server.yaml ./config/client.yaml ./config/params.yaml /opt/
COPY ./_entrypoint.sh /

ARG cloud_ip=127.0.0.1

ENV BRIDGE_SERVER=TRUE
ENV cloud_ip=$cloud_ip
ENV manage_port=26565
ENV ROS_DOMAIN_ID=0
ENV robot_name=cloi
ENV ROBOT_NAME=cloi

STOPSIGNAL SIGINT
STOPSIGNAL SIGSTOP

RUN echo "source "/opt/ros/$ROS_DISTRO/setup.bash"" >> /root/.bashrc
RUN chmod +x /_entrypoint.sh
ENTRYPOINT ["/_entrypoint.sh"]
