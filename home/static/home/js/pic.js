// assuming all images have the class thumb
$(".thumb").on("click",(e)=>{
    let clicked = e.target.id;
    let link = $("#main").attr("src");
    // all images must be of one format [png | jpg | gif]
    $("#main").attr("src",clicked+".png");
})