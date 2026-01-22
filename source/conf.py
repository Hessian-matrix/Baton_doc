# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sphinx_rtd_theme
html_theme = 'sphinx_rtd_theme'
html_show_sourcelink = False

project = 'Viobot2 User Manual'
# project = 'baton_doc'
copyright = '2024, hessian'
author = 'HessianMatrix'
release = '1.21'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'recommonmark',
    'sphinx_markdown_tables',
    'sphinx_rtd_theme'
]

templates_path = ['_templates']
exclude_patterns = [
    # Keep original Chinese docs in repo, but exclude them from the English build to avoid
    # duplicate/orphan pages and build warnings.
    'Viobot2简介.md',
    '开机指南.md',

    '基本功能介绍及使用/GNSS模块使用.md',
    '基本功能介绍及使用/NTP时间同步.md',
    '基本功能介绍及使用/双目深度.md',
    '基本功能介绍及使用/基本功能.md',
    '基本功能介绍及使用/工程应用上的相关配置.md',
    '基本功能介绍及使用/数据包录制.md',
    '基本功能介绍及使用/数据说明.md',
    '基本功能介绍及使用/版本更新.md',
    '基本功能介绍及使用/算法控制.md',
    '基本功能介绍及使用/重定位使用.md',

    '硬件接口使用/CAN通信.md',
    '硬件接口使用/I2C通信.md',
    '硬件接口使用/TF卡挂载.md',
    '硬件接口使用/串口通信.md',
    '硬件接口使用/网卡挂载与WiFi连接.md',
    '硬件接口使用/设备adb.md',

    'ROS_Master/ROS2多机通讯.md',
    'ROS_Master/ROS主从机配置.md',
    'ROS_Master/ROS多主机配置.md',

    'SDK测试例程/SDK_Demo.md',
    'SDK测试例程/SDK通信协议.md',

    'application/HM Inside.md',
    'application/HM Planner.md',
    'application/HM双目深度.md',
    'application/HM图像分割.md',
    'application/HM建图与重定位.md',

    '通用导航例程/ROS MoveBase.md',
    '通用导航例程/ROS2 Navigation2.md',

    '融合位姿/视觉融合单天线RTK.md',
    '融合位姿/视觉融合双天线RTK.md',

    '相关资料下载/代码仓库和链接汇总.md',
    'FAQ/常见问题.md',
]

language = "en"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

latex_engine = 'xelatex'

latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
'preamble': r'''
\addto\captionsenglish{\renewcommand{\chaptername}{}}
\usepackage[UTF8, scheme = plain]{ctex}
\setCJKmainfont{FandolSong-Regular.otf}
'''
}
