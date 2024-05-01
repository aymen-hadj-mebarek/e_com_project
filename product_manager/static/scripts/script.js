let slides = document.querySelectorAll('.slide');
let main_slide = document.querySelector('.main img')

let slide_right = document.querySelector('#slideR')
let slide_left = document.querySelector('#slideL')

let index = 0

main_slide.src = slides[index].src

slide_left.addEventListener("click", ()=>{
    if(index == slides.length){
        index = 0;
    }else{
        index ++;
    }
    main_slide.src = slides[index].src
});


slide_right.addEventListener("click", ()=>{
    if(index == 0){
        index = slides.length;
    }else{
        index --;
    }
    main_slide.src = slides[index].src
});
