# Django Task Management

📌 Overview（アプリ概要）

🖼️ Screenshots（画面）

🛠️ Tech Stack（使用技術）

🏗️ System Architecture（システム構成図）

🗄️ ER Diagram（ER図）
```mermaid
erDiagram

    CustomUser ||--o{ Task : creates

    CustomUser {
        int id PK
        string email
        string password_hash
        string display_name
    }

    Task {
        int id PK
        string title
        text description
        string status
        date due_date
        datetime created_at
        datetime updated_at
        int user_id FK
    }
```

✨ Features（機能一覧）

🚀 Getting Started（セットアップ）

🧪 Testing（テスト）

📂 Directory Structure（ディレクトリ構成）

🔮 Future Improvements（今後の改善予定）




