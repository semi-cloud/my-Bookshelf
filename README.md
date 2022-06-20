# my-Bookshelf

📚 _나만의 책장을 커스텀하고 기록하는 서비스, my-Bookshelf 입니다._

## 🛠 Stack
+ Django
+ Paas-TA

## 🔗 User Flow Diagram

<!-- <img width="518" alt="스크린샷 2022-06-20 오전 12 11 43" src="https://user-images.githubusercontent.com/71436576/174487900-b991cd5f-2e53-414b-a809-263660e8958d.png"> -->
<img width="518" src="https://user-images.githubusercontent.com/71436576/174487926-602d6c7f-7829-46f3-a6f5-5edd788e3be1.png">

## 🔗 상세 기능

<details>
<summary> 로그인 및 회원가입 </summary>
<div markdown="1">
  
  + 로그인 한 유저만 메인페이지에 접속 가능
</div>
</details>
  
<details>
<summary> 책 추가 </summary>
<div markdown="2">
  
  + 나의 책장에 추가하고 싶은 책을 검색하면 카카오 책 검색 API를 통해서 해당하는 모든 책 정보가 반환
  + 추가 버튼을 누르면, 기본 정보는 이미 입력되고 사용자는 후기, 별점, 태그만 추가(원하면 이미지도 다른 걸로 대체 가능)
  + 이때 원하는 태그가 없으면, 태그를 작성 페이지에서 바로 추가 가능
<div>
</details>
  
<details>
<summary> 책장 및 상세정보 페이지 조회 </summary>
<div markdown="3">
  
  + 메인페이지에서 나의 책장 조회 가능 (한 페이지당 4개 도서)
  + 더보기 버튼을 누르면 책 상세정보 페이지로 이동하며, 자기가 쓴 글에는 다른 사용자만 댓글을 달 수 있음
<div>
</details>
 
<details>
<summary> 책 수정 및 삭제 </summary>
<div markdown="4">

   + 자신이 쓴 글만 책 수정 및 삭제가 가능
<div>
</details>
  
<details>
<summary> 댓글 수정 및 삭제 </summary>
<div markdown="5">
  
   + 자신이 쓴 댓글에 대해서만 수정 및 삭제가 가능
<div>
</details>
  
<details>
<summary> 이웃 추가 및 조회 </summary>
<div markdown="6">
  
  + 모달에서 추가하고자 하는 이웃 이름 검색하고, 누르면 이웃 추가(자기 자신과,이미 팔로우 되어 있는 사용자는 불가능)
  + 메인페이지에 친구 목록 반환
  + 메인페이지에서 해당 이웃 이름을 누르면 이웃 책장으로 이동
<div>
</details>
  
<details>
<summary> 이웃 책장 및 상세정보 페이지 조회 </summary>
<div markdown="7">
  
  + 이웃 책장 페이지에서는 해당 이웃의 태그와 책 목록만 조획 가능
  + 해시태그를 추가할 수 없고, 이웃의 친구 목록을 볼 수 없음
<div>
</details>
  
<details>
<summary> 태그 추가 및 필터링 및 조회 </summary>
<div markdown="8">

  + 메인페이지에서 해시 태그 추가 가능
  + 메인페이지와 이웃 책장 페이지에서 태그별로 도서를 필터링 가능
  + 메인페이지에서 전체 태그를 조회
<div>
</details>
