# 1.Poll
## 1.1 Mối quan hệ:
poll -> n choice
1 câu hỏi có nhiều câu trả lời
## 1.2 Table:
### 1.2.1 poll:
* id:auto
* tilte:require
* options:list[Choice]-require
* created_at:datetime-auto
* expires_at:datetime | None


### 1.2.2 choice:
* description:require
* id:auto
* label:int require

## 1.3 Ví dụ:  
Title:Con gà có mấy chân  
Chọn câu trả lời options-Choice:  
1.yes  
2.no   
3.abstain   

Input code
```json
"options": [
        "yes",
        "no",
        "abstain"
    ]
```

Create code
 ```json
"options": [
            {
                "description": "yes",
                "id": "d8a6d6ee-91e7-46fd-948f-e018c8b880d4",
                "label": 1
            },
            {
                "description": "no",
                "id": "ec3873ce-d6de-4a5f-852c-7f208493b3b5",
                "label": 2
            },
            {
                "description": "abstain",
                "id": "3f6cd203-c64f-4253-ac37-34981f90a2fe",
                "label": 3
            }
        ]
```

## 1.4 Greate poll
Save with key 
```python
poll:{poll_id}
```
Create poll:
```json
{
    "title": "test vote 8",
    "options": [
        "yes",
        "no",
        "abstain"
    ],
    "expires_at": "2026-08-30T02:04:59.683Z"
}
```


response:
```json
{
    "detail": "Poll sucesss created",
    "poll_id": "b3e57ee5-9f74-467c-858c-48599624d2a8",
    "poll": {
        "title": "test vote 7",
        "options": [
            {
                "description": "yes",
                "id": "d8a6d6ee-91e7-46fd-948f-e018c8b880d4",
                "label": 1
            },
            {
                "description": "no",
                "id": "ec3873ce-d6de-4a5f-852c-7f208493b3b5",
                "label": 2
            },
            {
                "description": "abstain",
                "id": "3f6cd203-c64f-4253-ac37-34981f90a2fe",
                "label": 3
            }
        ],
        "expires_at": "2026-08-30T02:04:59.683000Z",
        "id": "b3e57ee5-9f74-467c-858c-48599624d2a8",
        "created_at": "2025-08-30T08:29:59.065750Z"
    }
}
```

# 2.Voter
## 2.1 Mối quan hệ
1 người có thể vote cho nhiều poll  
1 voter-> n poll
voter chi có email và voted_at-ngày bình chọn
## 2.2 Table
### 2.2.1 VoterCreate
* email: EmailStr->require


### 2.2.2 Voter-voter
* email:required
* voted_at:datetime-auto
 

### 2.2.3 Vote
* poll_id: UUID-require
* choice_id: UUID-require
* voter: Voter-require


## 2.3 Create vote
### 2.3.1 VoteById
* choice_id: UUID-require
* voter: VoterCreate-require


### 2.3.2 VoteByLabel
* choice_label: int-require
* voter: VoterCreate-require


## 2.4 Code demo
### 2.4.1 Create vote by id
input data
```json
{
    "choice_id": "f4ce92a8-cc7c-4b7c-a7b4-4fcc382f5bbf",
    "voter": {
        "email": "user@example.com"
    }
}
```

response:
```json
{
    "message": "Vote recorded",
    "vote": {
        "poll_id": "3167b140-bd58-4e7c-bd1c-775a1e9537f2",
        "choice_id": "f4ce92a8-cc7c-4b7c-a7b4-4fcc382f5bbf",
        "voter": {
            "email": "user@example.com",
            "voted_at": "2025-08-30T21:39:33.604099"
        }
    }
}
```
### 2.4.2 Create vote by label
input data
```json
{
    "choice_label": 1,
    "voter": {
        "email": "user@example.com"
    }
}
```

response:
```json
{
    "message": "Vote recorded",
    "vote": {
        "poll_id": "3167b140-bd58-4e7c-bd1c-775a1e9537f2",
        "choice_id": "424e0d8a-d3ca-4611-ba56-045b296d15d3",
        "voter": {
            "email": "user@example.com",
            "voted_at": "2025-08-30T21:45:37.668342"
        }
    }
}
```
## 2.5 save vote use hash stored redis
Save with key 
```python
votes:{poll_id}
```

### 2.5.1 save vote with
poll_id,email,vote_json_data

```python
def save_vote(poll_id: UUID, vote: Vote) -> None:
    vote_json = vote.model_dump_json()
    redis_client.hset(f"votes:{poll_id}", vote.voter.email, vote_json)
```
### 2.5.2 get vote with
poll_id,email

```python
def get_vote(poll_id: UUID, email: str) -> Vote | None:
    vote_json = redis_client.hget(f"votes:{poll_id}", email)

    if vote_json:
        return Vote.model_validate_json(vote_json)

    return None
```

### 2.5.3 Check create vote trùng nhau with
poll_id,email

```python
if utils.get_vote(poll_id, vote.voter.email):
        raise HTTPException(status_code=400, detail="Already voted")
```


