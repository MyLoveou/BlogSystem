# 数据库设计与API设计
*   ## 个人博客系统后端设计
    
    ## 数据库设计
    
    ### 核心数据表
    
    | 表名  | 字段  | 类型  | 描述  |
    | --- | --- | --- | --- |
    | **articles** | id  | UUID | 文章唯一标识符 |
    |     | title | VARCHAR(200) | 文章标题 |
    |     | slug | VARCHAR(200) | URL友好标识符 |
    |     | author\_id | FK(users) | 作者ID |
    |     | content | TEXT | Markdown内容 |
    |     | html\_content | TEXT | 渲染后的HTML内容 |
    |     | excerpt | TEXT | 文章摘要 |
    |     | cover\_image | VARCHAR(255) | 封面图路径 |
    |     | status | ENUM('draft','published','archived') | 文章状态 |
    |     | views | INT | 浏览量 |
    |     | toc | JSON | 目录结构 |
    |     | created\_at | DATETIME | 创建时间 |
    |     | updated\_at | DATETIME | 更新时间 |
    |     | published\_at | DATETIME | 发布时间 |
    
    | **categories** | id  | INT | 分类ID |
    | --- | --- | --- | --- |
    |     | name | VARCHAR(100) | 分类名称 |
    |     | slug | VARCHAR(100) | URL友好标识符 |
    |     | description | TEXT | 分类描述 |
    |     | parent\_id | FK(categories) | 父分类ID |
    |     | created\_at | DATETIME | 创建时间 |
    
    | **tags** | id  | INT | 标签ID |
    | --- | --- | --- | --- |
    |     | name | VARCHAR(50) | 标签名称 |
    |     | slug | VARCHAR(50) | URL友好标识符 |
    |     | color | VARCHAR(7) | 标签颜色 |
    |     | usage\_count | INT | 使用次数 |
    |     | created\_at | DATETIME | 创建时间 |
    
    | **article\_category** | article\_id | FK(articles) | 文章ID |
    | --- | --- | --- | --- |
    |     | category\_id | FK(categories) | 分类ID |
    
    | **article\_tag** | article\_id | FK(articles) | 文章ID |
    | --- | --- | --- | --- |
    |     | tag\_id | FK(tags) | 标签ID |
    
    ### 系统配置表
    
    | 表名  | 字段  | 类型  | 描述  |
    | --- | --- | --- | --- |
    | **site\_settings** | id  | INT | 设置ID |
    |     | site\_name | VARCHAR(100) | 网站名称 |
    |     | site\_slogan | VARCHAR(200) | 网站标语 |
    |     | motto | VARCHAR(300) | 座右铭 |
    |     | avatar | VARCHAR(255) | 头像路径 |
    |     | footer\_text | TEXT | 页脚文本 |
    |     | github\_url | VARCHAR(255) | GitHub链接 |
    |     | twitter\_url | VARCHAR(255) | Twitter链接 |
    |     | linkedin\_url | VARCHAR(255) | LinkedIn链接 |
    |     | email | VARCHAR(100) | 联系邮箱 |
    |     | created\_at | DATETIME | 创建时间 |
    |     | updated\_at | DATETIME | 更新时间 |
    
    | **pages** | id  | INT | 页面ID |
    | --- | --- | --- | --- |
    |     | page\_type | ENUM('about','friend') | 页面类型 |
    |     | title | VARCHAR(100) | 页面标题 |
    |     | content | TEXT | Markdown内容 |
    |     | html\_content | TEXT | 渲染后的HTML |
    |     | created\_at | DATETIME | 创建时间 |
    |     | updated\_at | DATETIME | 更新时间 |
    
    ### 辅助数据表
    
    | 表名  | 字段  | 类型  | 描述  |
    | --- | --- | --- | --- |
    | **friend\_links** | id  | INT | 友链ID |
    |     | name | VARCHAR(100) | 友链名称 |
    |     | url | VARCHAR(255) | 链接地址 |
    |     | description | VARCHAR(200) | 描述  |
    |     | is\_active | BOOLEAN | 是否激活 |
    |     | created\_at | DATETIME | 创建时间 |
    
    | **image\_uploads** | id  | UUID | 图片ID |
    | --- | --- | --- | --- |
    |     | image | VARCHAR(255) | 图片路径 |
    |     | uploaded\_by | FK(users) | 上传者 |
    |     | uploaded\_at | DATETIME | 上传时间 |
    
    | **weather\_cache** | id  | INT | 缓存ID |
    | --- | --- | --- | --- |
    |     | location | VARCHAR(100) | 位置  |
    |     | data | JSON | 天气数据 |
    |     | last\_updated | DATETIME | 最后更新时间 |
    |     | expires\_at | DATETIME | 过期时间 |
    
    ## API 设计
    
    ### 文章相关 API
    
    | 端点  | 方法  | 描述  | 参数  | 认证  |
    | --- | --- | --- | --- | --- |
    | `/api/articles/` | GET | 获取文章列表 | `category`, `tag`, `author`, `status`, `year`, `month`, `search`, `page`, `page_size` | 否   |
    | `/api/articles/{id}/` | GET | 获取单篇文章 | \-  | 否   |
    | `/api/articles/` | POST | 创建新文章 | `title`, `content`, `excerpt`, `cover_image`, `category[]`, `tags[]`, `status` | 是   |
    | `/api/articles/{id}/` | PUT | 更新文章 | 同上  | 是   |
    | `/api/articles/{id}/` | DELETE | 删除文章 | \-  | 是   |
    | `/api/articles/{id}/related/` | GET | 获取相关文章 | \-  | 否   |
    
    ### 分类与标签 API
    
    | 端点  | 方法  | 描述  | 参数  | 认证  |
    | --- | --- | --- | --- | --- |
    | `/api/categories/` | GET | 获取所有分类 | \-  | 否   |
    | `/api/categories/{slug}/articles/` | GET | 获取分类下的文章 | `page`, `page_size` | 否   |
    | `/api/tags/` | GET | 获取所有标签 | \-  | 否   |
    | `/api/tags/{slug}/articles/` | GET | 获取标签下的文章 | `page`, `page_size` | 否   |
    
    ### 时间线与归档 API
    
    | 端点  | 方法  | 描述  | 参数  | 认证  |
    | --- | --- | --- | --- | --- |
    | `/api/timeline/` | GET | 获取时间线格式的文章 | \-  | 否   |
    | `/api/archives/` | GET | 获取按年月归档的文章 | \-  | 否   |
    
    ### 系统配置 API
    
    | 端点  | 方法  | 描述  | 参数  | 认证  |
    | --- | --- | --- | --- | --- |
    | `/api/settings/` | GET | 获取站点设置 | \-  | 否   |
    | `/api/settings/` | PUT | 更新站点设置 | `site_name`, `site_slogan`, `motto`, `avatar`, `footer_text`, `github_url`, `twitter_url`, `linkedin_url`, `email` | 是   |
    | `/api/pages/about/` | GET | 获取关于页面 | \-  | 否   |
    | `/api/pages/friend/` | GET | 获取友链页面 | \-  | 否   |
    | `/api/friendlinks/` | GET | 获取所有友链 | \-  | 否   |
    
    ### 媒体与实用工具 API
    
    | 端点  | 方法  | 描述  | 参数  | 认证  |
    | --- | --- | --- | --- | --- |
    | `/api/upload/image/` | POST | 上传图片 | `image` (文件) | 是   |
    | `/api/weather/` | GET | 获取天气信息 | `location` | 否   |
    | `/api/markdown/render/` | POST | 渲染Markdown | `content` | 否   |
    
    ## API 响应示例
    
    ### 获取文章列表 (GET /api/articles/)
    
    ```json
    {
      "count": 125,
      "next": "https://api.example.com/api/articles/?page=2",
      "previous": null,
      "results": [
        {
          "id": "550e8400-e29b-41d4-a716-446655440000",
          "title": "Vue3高级技巧",
          "slug": "vue3-advanced-techniques",
          "excerpt": "探索Vue3中的高级编程模式...",
          "cover_image": "/media/article_covers/vue3.jpg",
          "views": 1024,
          "published_at": "2023-10-15T08:30:00Z",
          "author": {
            "id": 1,
            "username": "tech_writer"
          },
          "categories": [
            {"id": 2, "name": "前端开发"}
          ],
          "tags": [
            {"id": 5, "name": "Vue", "color": "#42b883"}
          ]
        }
      ]
    }
    ```
    
    ### 获取单篇文章 (GET /api/articles/{id}/)
    
    ```json
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Vue3高级技巧",
      "slug": "vue3-advanced-techniques",
      "content": "# Vue3高级技巧\n\n探索Vue3中的高级编程模式...",
      "html_content": "<h1>Vue3高级技巧</h1><p>探索Vue3中的高级编程模式...</p>",
      "excerpt": "探索Vue3中的高级编程模式...",
      "cover_image": "/media/article_covers/vue3.jpg",
      "status": "published",
      "views": 1024,
      "toc": [
        {"level": 1, "id": "composition-api", "name": "Composition API"},
        {"level": 2, "id": "setup-function", "name": "setup函数"}
      ],
      "created_at": "2023-10-10T14:30:00Z",
      "updated_at": "2023-10-12T09:15:00Z",
      "published_at": "2023-10-15T08:30:00Z",
      "author": {
        "id": 1,
        "username": "tech_writer",
        "first_name": "张",
        "last_name": "三"
      },
      "categories": [
        {"id": 2, "name": "前端开发", "slug": "frontend"}
      ],
      "tags": [
        {"id": 5, "name": "Vue", "slug": "vue", "color": "#42b883"},
        {"id": 8, "name": "JavaScript", "slug": "javascript", "color": "#f7df1e"}
      ]
    }
    ```
    
    ### 获取时间线数据 (GET /api/timeline/)
    
    ```json
    {
      "2023": {
        "10": [
          {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Vue3高级技巧",
            "slug": "vue3-advanced-techniques",
            "published_at": "2023-10-15T08:30:00Z"
          },
          {
            "id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
            "title": "Django性能优化",
            "slug": "django-performance",
            "published_at": "2023-10-08T14:20:00Z"
          }
        ],
        "9": [
          {
            "id": "6ba7b811-9dad-11d1-80b4-00c04fd430c8",
            "title": "响应式设计实践",
            "slug": "responsive-design",
            "published_at": "2023-09-22T10:15:00Z"
          }
        ]
      },
      "2022": {
        "12": [
          {
            "id": "6ba7b812-9dad-11d1-80b4-00c04fd430c8",
            "title": "年度技术回顾",
            "slug": "year-review-2022",
            "published_at": "2022-12-30T16:45:00Z"
          }
        ]
      }
    }
    ```
    
    ## 关键功能说明
    
    ### 文章管理
    
    1.  Markdown内容存储和渲染处理
    2.  自动生成文章目录结构（TOC）
    3.  多维度文章筛选（分类、标签、作者、状态、日期）
    4.  浏览量自动统计
    
    ### 分类与标签
    
    1.  多级分类支持（父子关系）
    2.  标签颜色标记和热度统计
    3.  基于slug的URL友好标识
    
    ### 系统配置
    
    1.  单例站点设置管理
    2.  独立页面管理（关于页、友链页）
    3.  Markdown内容支持
    
    ### 实用工具
    
    1.  图片上传与管理
    2.  天气数据缓存服务
    3.  Markdown渲染API
    
    ### 性能优化
    
    1.  分页支持
    2.  查询优化（索引、预取相关数据）
    3.  天气数据缓存机制
    4.  常用数据缓存策略
    
    这个设计提供了完整的后端架构，支持前端Vue博客系统的所有功能需求，包括文章管理、分类标签、系统配置和实用工具等。API设计遵循RESTful原则，数据结构清晰，便于前端集成。