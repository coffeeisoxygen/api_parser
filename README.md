# Project API Parser

Project ini adalah sebauh localhost yg akan menjembatani antara Otomax (Requester) dengan Addon Yang du develop otoplus :
    - digipos : adddon telkomsel
    - isimple : adddon indosat
    - sidompul : addon XL
    - Rita : addon tri
    - dan addon addon lain nya

## Features

- memparse ulang respon dari addon yang panjang , menjadi simple string ke otomax
- menampilkan UI dengan streamlit untuk terkoneksi ke adddon (seperti get account dan lain lain)
- dan feature lainnya

## Flow

berikut diagram use case dari project ini:

```mermaid
sequenceDiagram
    autonumber
    participant O as Otomax
    participant A as Addon
    participant P as API Parser

    O->>P: Request data
    P->>A: Forward request
    A-->>P: Response data
    P-->>O: Parsed response data
```

## Tech Stack

- UV : sebagai pengganti pip untuk management project.
- Python >= 3.12 : versi python yang digunakan.
- FastAPI : untuk membuat API yang cepat dan efisien.
- Loguru : untuk logging yang lebih baik.

## sementara NO FrontEND dulu , ngga ada Crud by UI

## validation chain

```mermaid
stateDiagram
    direction LR
    [*] --> IP_Whitelist_Check
    IP_Whitelist_Check --> Member_Check : ✅ IP Valid
    IP_Whitelist_Check --> Failed : ❌ IP Not Allowed

    Member_Check --> Credential_Check : ✅ Member Found
    Member_Check --> Failed : ❌ Member Not Found

    Credential_Check --> Success : ✅ Auth OK
    Credential_Check --> Failed : ❌ Signature / PIN Error

    Success --> [*]
    Failed --> [*]
```
