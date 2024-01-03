async function showCupcakes() {
    const res = await axios.get("http://127.0.0.1:5000/api/cupcakes")
    console.log(res)
    for(let cupcake of res.data){
        let newCupcake = $(makeCupcakeHTML(cupcake))
        $("#cupcake-list").append(newCupcake)
    }
}

function makeCupcakeHTML(cupcake) {
    console.log(cupcake)
    return `
    <div data-id=${cupcake.id}>
    <li>
       <img src="${cupcake.image}" alt="Cupcake" class="img-thumbnail" style="width: 150px; border-radius:10px;">
       <p><b>Flavor:</b> ${cupcake.flavor}</p>
       <p><b>Size:</b> ${cupcake.size}</p>
       <p><b>Rating:</b> ${cupcake.rating}</p>
    </li>
    <button class="delete-btn btn btn-danger">X</button>
    </div>`

}

$("#cupcake-form").on("submit", async function(e) {
    e.preventDefault()
    let flavor = $("#flavor-input").val()
    let size = $("#size-input").val()
    let rating = $("#rating-input").val()
    let image = $("#image-input").val()

    const newCupcakeRes = await axios.post("http://127.0.0.1:5000/api/cupcakes", {
        flavor,
        size,
        rating,
        image
    })
    let newCupcake = $(makeCupcakeHTML(newCupcakeRes.data))
    $("#cupcake-list").append(newCupcake)
    $("#cupcake-form").trigger("reset")
})

$("#cupcake-list").on("click", ".delete-btn", async function (evt){
    evt.preventDefault()
    let $cupcake = $(evt.target).closest("div")
    let cupcakeId = $cupcake.attr("data-id")
    await axios.delete(`http://127.0.0.1:5000/api/cupcakes/${cupcakeId}`)
    $cupcake.remove()
})

$(showCupcakes)