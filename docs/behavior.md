
POST /users:
* user資料缺失、格式錯誤或user類型不屬於 [`買家`, `賣家`]：回傳422錯誤

POST /users/signIn：
* 帳號不存在：回傳401錯誤
* 密碼錯誤：回傳401錯誤

GET /users/me:
* JWT認證失敗：回傳401錯誤
* JWT user ID不存在：回傳404錯誤

PATCH /users/{id}:
* JWT認證失敗：回傳401錯誤
* user資料缺失、格式錯誤或user類型不屬於 [`買家`, `賣家`]：回傳422錯誤
* 修改自己以外的user資料：回傳403錯誤

POST /products:
* JWT認證失敗：回傳401錯誤
* product資料缺失或格式錯誤：回傳422錯誤


GET /products:
* 無

PATCH /products/{id}:
* JWT認證失敗：回傳401錯誤
* 修改不屬於自己的product：回傳403錯誤
* product資料缺失或格式錯誤：回傳422錯誤

GET /products/{id}:
* ID不存在：回傳404錯誤

DELETE /products/{id}:
* JWT認證失敗：回傳401錯誤
* ID不存在：回傳404錯誤
* 刪除不屬於自己的product：回傳403錯誤


POST /orders:
* JWT認證失敗：回傳401錯誤
* order資料缺失或格式錯誤：回傳422錯誤

GET /orders/{id}:
* JWT認證失敗：回傳401錯誤
* ID不存在：回傳404錯誤
* Access不屬於自己的order：回傳403錯誤

GET /orders:
* JWT認證失敗：回傳401錯誤

POST /images:
* JWT認證失敗：回傳401錯誤
* 上傳圖床失敗：回傳500錯誤
