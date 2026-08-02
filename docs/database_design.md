```mermaid
erDiagram

ROLE ||--o{ USER : has

CATEGORY ||--o{ PRODUCT : contains

USER ||--o{ BEHAVIOR_EVENT : generates

USER ||--o{ RECOMMENDATION : receives

USER ||--o{ WISHLIST : owns

USER ||--o{ BOOKMARK : owns

PRODUCT ||--o{ WISHLIST : saved

PRODUCT ||--o{ BOOKMARK : bookmarked

PRODUCT }o--o{ RECOMMENDATION : recommended

RECOMMENDATION ||--o{ FEEDBACK : has
```