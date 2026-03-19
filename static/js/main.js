document.addEventListener("DOMContentLoaded", function () {

console.log("video platform loaded")

setupLikeButtons()

setupCommentForm()

setupVideoPreview()

})

document.addEventListener("contextmenu", function(e){
    if(e.target.tagName === "VIDEO"){
        e.preventDefault();
    }
});

document.addEventListener("touchstart", function(e){
    if(e.target.tagName === "VIDEO"){
        e.preventDefault();
    }
});

document.addEventListener("DOMContentLoaded", function() {
    const cards = document.querySelectorAll(".video-frame-a");

    cards.forEach(card => {
        const preview = card.querySelector(".hover-preview");
        const thumb = card.querySelector("img.video-thumb");

        if (!preview) return;

        card.addEventListener("mouseenter", () => {
            if (thumb) thumb.style.display = "none";
            preview.style.display = "block";
            preview.play();
        });

        card.addEventListener("mouseleave", () => {
            if (thumb) thumb.style.display = "block";
            preview.pause();
            preview.currentTime = 0;
            preview.style.display = "none";
        });
    });
});


document.addEventListener("DOMContentLoaded", function() {

    const sideCards = document.querySelectorAll(".side-thumb");

    sideCards.forEach(card => {
        const preview = card.querySelector(".hover-preview");
        const thumb = card.querySelector("img.video-thumb");

        if (!preview) return;

        card.addEventListener("mouseenter", () => {
            if (thumb) thumb.style.display = "none"; 
            preview.style.display = "block"; 
            preview.play();
        });

        card.addEventListener("mouseleave", () => {
            if (thumb) thumb.style.display = "block"; 
            preview.pause();
            preview.currentTime = 0;
            preview.style.display = "none"; 
        });
    });
});

// document.addEventListener("DOMContentLoaded", function(){

//     const descContainer = document.getElementById("video-description");
//     const descText = document.getElementById("description-text");
//     const toggleBtn = document.getElementById("toggle-desc");

//     if(toggleBtn){
//         toggleBtn.addEventListener("click", function(){
//             if(descContainer.style.maxHeight === "none"){
//                 descContainer.style.maxHeight = "120px";
//                 toggleBtn.textContent = "Show More";
//             } else {
//                 descContainer.style.maxHeight = "none";
//                 toggleBtn.textContent = "Show Less";
//             }
//         });
//     }

// });

function setupLikeButtons(){

    const likeButtons=document.querySelectorAll(".like-btn")

    likeButtons.forEach(btn=>{

        btn.addEventListener("click",function(e){

            e.preventDefault()

            const videoId=this.dataset.video

            fetch("/like/"+videoId)
            .then(res=>res.text())
            .then(()=>{

                console.log("liked video",videoId)

            })

        })

    })

}

function setupCommentForm(){

    const form=document.querySelector("#comment-form")

    if(!form) return

    form.addEventListener("submit",function(e){

        const input=document.querySelector("#comment-input")

        if(input.value.trim()===""){

            e.preventDefault()

            alert("comment cannot be empty")

        }

    })

}

function setupVideoPreview(){

const cards=document.querySelectorAll(".video-card")

cards.forEach(card=>{

const video=card.querySelector("video")

if(!video) return

card.addEventListener("mouseenter",()=>{

video.play()

})

card.addEventListener("mouseleave",()=>{

video.pause()
video.currentTime=0

})

})

}