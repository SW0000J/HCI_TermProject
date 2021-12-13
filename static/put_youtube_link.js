function getYoutubeLink() {
    const youtube_link = document.getElementById("get_youtube_link").value;
    document.getElementById("use_youtube_link").innerHTML = youtube_link;
    console.log(youtube_link);
}