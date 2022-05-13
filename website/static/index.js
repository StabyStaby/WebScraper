// $(document).ready(function(){
//     $("#select").change(function(){
//       let cate=$(this).val();
//       if (cate!=''){
//         $.ajax({
//           url:"{{url_for('getDataAjax')}}",
//           type:"POST",
//           data:{"data":cate},
//           success:function(res){
//             $("#courses").html(res);
//           }
//         });
//       }else{
//         $("#courses").html("");
//       }
//     });
//   });

// function changeUser(noteId){
//     fetch('/delete-note',{
//         method : 'POST',
//         body : JSON.stringify({noteId:noteId}),
//     }).then((_res)=>{
//         window.location.href = "/";
//     });
// }


function changeUser(){
  var slc = $( "#select" ).val();
  fetch('/changeUser',{
      method : 'POST',
      body : JSON.stringify({user:slc}),
  }).then((_res)=>{
      console.log(_res)
      window.location.href = _res.url;
  });
}

function deletManga(mangaId){
  var url = window.location.href
  fetch('/delete-manga',{
      method : 'POST',
      body : JSON.stringify({mangaId:mangaId,url:url}),
  }).then((_res)=>{
      window.location.href = _res.url;
  });
}