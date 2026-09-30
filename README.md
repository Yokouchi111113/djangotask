# Django Task Management

Python • Django • Django REST Framework • PostgreSQL • Docker • Playwright • pytest

📌 Overview

Django REST Frameworkを用いてREST APIを構築し、JWT認証を実装したタスク管理アプリです。

Docker Compose・PostgreSQLを用いた開発環境を構築しています。

また、pytestによるAPIテストとPlaywrightによるE2Eテストを実装し、主な機能の動作を確認しています。

🛠️ Tech Stack
| 分類 | 技術 |
|------|------|
| 言語 | Python, JavaScript, HTML, CSS |
| バックエンド | Django, Django REST Framework |
| 認証 | JWT (SimpleJWT) |
| データベース | PostgreSQL |
| テスト | pytest (API Test), Playwright (E2E Test) |
| 開発環境 | Docker, Docker Compose |
| パッケージ管理 | pip, npm |

✨ Features
- ユーザー登録
- ログイン/ログアウト
- タスクの作成・一覧表示・編集・削除（CRUD）
- キーワード検索
- 期限検索
- ステータス管理（未着手・進行中・完了）
- 期限日の設定
- ユーザーごとのタスク管理

🖼️ Screenshots
![トップページ](images/top.png)

🏗️ System Architecture

```mermaid
graph LR

    User["👤 User"]

    subgraph Docker Compose
        Browser["🌐 Browser"]
        Web["🐍 Django REST Framework<br/>SimpleJWT"]
        DB["🐘 PostgreSQL"]
    end

    User --> Browser
    Browser -->|"HTTP / Fetch API"| Web
    Web --> DB

    Playwright["🎭 Playwright"]
    Playwright --> Browser
```
🗄️ ER Diagram
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

🧪 Testing
### テスト設計・テストケース

- 機能・テスト観点・テスト技法を整理したテスト設計を作成
- テスト設計に基づき、正常系・異常系・境界値などのテストケースを作成
- テストケースを実行し、実行結果と判定を記録

- ### テスト成果物

テスト設計、テストケース・実行結果、自動テスト対応表、バグ報告を
Excelにまとめています。

- [テスト設計・テストケース・自動テスト対応表・バグ報告](docs/テスト設計・テストケース・自動テスト対応表・バグ報告.xlsx)

### 探索的テスト・不具合

- テストケースに含まれていない操作や組み合わせを探索的に確認
- 仕様として想定していなかった挙動を発見
- 発見した問題について、再現手順・期待結果・実際の結果を整理

### 自動テストの方針

繰り返し実行可能にすることで、機能変更時の回帰確認を効率化

- **Playwright**：ユーザー登録、ログイン、タスクCRUD、検索など、ユーザー操作を伴う主な画面機能
- **pytest**：APIの認証・認可、バリデーション、CRUD、検索など、APIレベルで繰り返し確認できる処理
- 境界値や異常系についても、主な機能については自動テストの対象とした
- 画面上の細かな表示確認や探索的テストなど、自動化の効果が低いものは手動テストとして実施

### APIテスト

- pytestによるAPIテストを実装
- サインアップ、サインイン、タスクCRUD、キーワード検索・期限検索、バリデーション、権限を検証
- 34件のテストケースを実装

### E2Eテスト

- PlaywrightによるE2Eテストを実装
- サインアップ、サインイン、タスクCRUD、キーワード検索・期限検索を検証
- 28件のテストシナリオをChromium・Firefox・WebKitの3ブラウザで実行

### 自動テストとの対応

手動テストケースと自動テストの対応関係を整理し、
どのテストケースを自動化しているかを確認できるようにした。

- Playwright：画面操作を中心としたE2Eテスト
- pytest：API・認証認可・バックエンド処理を中心としたテスト
- 一部のテストケースは手動確認として残し、自動テストとの対応を整理

### 実行環境

- Dockerコンテナ上でpytestおよびPlaywrightを実行可能

　　### 実行コマンド
   
    ```bash
    docker compose exec web pytest
    ```
　　
    ```bash
    docker compose run --rm playwright
    ```

🚀 Getting Started
### 前提条件

- Docker
- Docker Compose

### 1. リポジトリをクローン

```bash
git clone https://github.com/Yokouchi111113/djangotask.git
cd djangotask
```

### 2. 環境変数を設定

`.env.example` をコピーして `.env` を作成します。

**Windows (PowerShell)**

```powershell
copy .env.example .env
```

**Linux / macOS**

```bash
cp .env.example .env
```

必要に応じて `.env` 内の `SECRET_KEY` や `POSTGRES_PASSWORD` を変更してください。

### 3. コンテナを起動

```bash
docker compose up --build
```

### 4. データベースをマイグレーション

```bash
docker compose exec web python manage.py migrate
```

### 5. アプリへアクセス

ブラウザで以下にアクセスしてください。

```
http://localhost:8000
```

📂 Directory Structure
```
djangotask/
├── config/                 # Django project
│   ├── accounts/           # User authentication
│   ├── task/               # Task management app
│   │     └─tests/          # pytest
│   ├── templates/          # HTML templates
│   ├── e2e/                # Playwright tests
│   ├── config/             # Django settings
│   ├── manage.py
│   ├── package.json
│   └── playwright.config.js
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

💡 Highlights
- Django REST Frameworkを用いてREST APIを設計
- JWT認証（SimpleJWT）による認証機能を実装
- Docker Composeで開発・テスト環境を構築
- pytestによるAPIテストを作成
- PlaywrightによるE2Eテストを実装し、Chromium・Firefox・WebKitの3ブラウザで動作を確認
- Playwrightの共通処理（サインアップ・サインイン・タスク作成など）を関数化し、保守性を向上

🔮 Future Improvements
- GitHub Actionsを用いたCIの構築（pytest・Playwrightの自動実行）
- 本番環境へのデプロイ
- UI/UXの改善
