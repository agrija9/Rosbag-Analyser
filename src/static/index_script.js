async function uploadFunction(){
    var bagfile =  String(document.getElementById("file_name").value);
    if (bagfile.substring(bagfile.length - 4, bagfile.length) == ".bag"){
        document.getElementById("loader").style.display = "block";
        document.getElementById("dropContainer").style.display = "none";
        document.getElementById("file_name").style.display = "none";
        document.getElementById("btnSubmit").style.display = "none";
        document.getElementById("btnSubmit1").style.display = "none";
    }else{
        document.getElementById("btnSubmit").disabled = true;
        alert("The visualizer will only accept .bag files!");
        await new Promise(resolve => setTimeout(resolve, 100));
        document.getElementById("btnSubmit").disabled = false;
    }
}

dropContainer.ondragover = dropContainer.ondragenter = function(evt) {
    evt.preventDefault();
    document.getElementById("filename").innerHTML = 'Drag Here...';
    document.getElementById("dropContainer").style.border = "5px dashed green";
    document.getElementById("dropContainer").style.background = "#dbbdba";
};

dropContainer.ondragleave = dropContainer.ondragleave = function(evt) {
    evt.preventDefault();
    document.getElementById("filename").innerHTML = 'Drag one or more files to this Drop Zone ...';
    document.getElementById("dropContainer").style.border = "5px dashed grey";
    document.getElementById("dropContainer").style.background = "white";
};

dropContainer.ondrop = function(evt) {
    file_name.files = evt.dataTransfer.files;
    document.getElementById("filename").innerHTML = file_name.files[0].name;
    evt.preventDefault();
};