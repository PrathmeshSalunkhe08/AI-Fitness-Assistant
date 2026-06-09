// document.addEventListener("DOMContentLoaded", function () {

//     const input = document.getElementById("foodInput");
//     const suggestionBox = document.getElementById("suggestions");
//     const calculateBtn = document.getElementById("calculateBtn");

//     let chartInstance = null;

//     input.addEventListener("input", async function () {

//         const query = input.value;

//         if (query.length < 2) {
//             suggestionBox.innerHTML = "";
//             return;
//         }

//         const response = await fetch("/search_food", {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify({ query: query })
//         });

//         const data = await response.json();
//         suggestionBox.innerHTML = "";

//         data.forEach(function (item) {
//             const div = document.createElement("div");
//             div.innerText = item;

//             div.onclick = function () {
//                 input.value = item;
//                 suggestionBox.innerHTML = "";
//             };

//             suggestionBox.appendChild(div);
//         });
//     });


//     calculateBtn.addEventListener("click", async function () {

//         const food = input.value;
//         const quantity = document.getElementById("quantityInput").value;

//         if (!food || !quantity) {
//             alert("Enter food and quantity");
//             return;
//         }

//         const response = await fetch("/calculate_nutrition", {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify({
//                 food: food,
//                 quantity: quantity
//             })
//         });

//         const data = await response.json();

//         if (data.error) {
//             alert(data.error);
//             return;
//         }

//         document.getElementById("result").innerHTML = `
//             Calories: ${data.calories.toFixed(2)} kcal <br>
//             Protein: ${data.protein.toFixed(2)} g <br>
//             Carbs: ${data.carbs.toFixed(2)} g <br>
//             Fat: ${data.fat.toFixed(2)} g
//         `;

//         drawChart(data);
//     });


//     function drawChart(data) {

//         const ctx = document.getElementById("nutritionChart").getContext("2d");

//         if (chartInstance) {
//             chartInstance.destroy();
//         }

//         chartInstance = new Chart(ctx, {
//             type: "bar",
//             data: {
//                 labels: ["Protein", "Carbs", "Fat"],
//                 datasets: [{
//                     data: [data.protein, data.carbs, data.fat],
//                     backgroundColor: ["#00c6ff", "#f7971e", "#ff512f"],
//                     borderRadius: 8
//                 }]
//             },
//             options: {
//                 plugins: {
//                     legend: { display: false }
//                 },
//                 scales: {
//                     x: { ticks: { color: "white" } },
//                     y: { ticks: { color: "white" } }
//                 }
//             }
//         });
//     }

// });
// document.addEventListener("DOMContentLoaded", function () {
//     const input = document.getElementById("foodInput");
//     const suggestionBox = document.getElementById("suggestions");
//     const calculateBtn = document.getElementById("calculateBtn");

//     let chartInstance = null;

//     // Debounce function to limit API calls
//     function debounce(func, delay) {
//         let timeout;
//         return function (...args) {
//             clearTimeout(timeout);
//             timeout = setTimeout(() => func.apply(this, args), delay);
//         };
//     }

//     // Debounced input handler for suggestions
//     const debouncedInput = debounce(async function () {
//         const query = input.value;

//         if (query.length < 2) {
//             suggestionBox.innerHTML = "";
//             return;
//         }

//         try {
//             const response = await fetch("/search_food", {
//                 method: "POST",
//                 headers: { "Content-Type": "application/json" },
//                 body: JSON.stringify({ query: query })
//             });

//             const data = await response.json();
//             suggestionBox.innerHTML = "";

//             data.forEach(function (item) {
//                 const div = document.createElement("div");
//                 div.innerText = item;

//                 div.onclick = function () {
//                     input.value = item;
//                     suggestionBox.innerHTML = "";
//                 };

//                 suggestionBox.appendChild(div);
//             });
//         } catch (error) {
//             console.error("Error fetching suggestions:", error);
//             // Optional: Show a subtle error, but keep it non-disruptive
//         }
//     }, 300);

//     input.addEventListener("input", debouncedInput);

//     calculateBtn.addEventListener("click", async function () {
//         const food = input.value;
//         const quantity = document.getElementById("quantityInput").value;

//         if (!food || !quantity) {
//             alert("Enter food and quantity"); // Kept as is for simplicity, but could be enhanced to inline
//             return;
//         }

//         // Loading state
//         calculateBtn.disabled = true;
//         calculateBtn.innerHTML = '<span class="spinner"></span> Calculating...';

//         try {
//             const response = await fetch("/calculate_nutrition", {
//                 method: "POST",
//                 headers: { "Content-Type": "application/json" },
//                 body: JSON.stringify({
//                     food: food,
//                     quantity: quantity
//                 })
//             });

//             const data = await response.json();

//             if (data.error) {
//                 alert(data.error);
//                 return;
//             }

//             document.getElementById("result").innerHTML = `
//                 Calories: ${data.calories.toFixed(2)} kcal <br>
//                 Protein: ${data.protein.toFixed(2)} g <br>
//                 Carbs: ${data.carbs.toFixed(2)} g <br>
//                 Fat: ${data.fat.toFixed(2)} g
//             `;

//             drawChart(data);
//         } catch (error) {
//             console.error("Error calculating nutrition:", error);
//             alert("Failed to calculate nutrition. Please try again.");
//         } finally {
//             // Reset button
//             calculateBtn.disabled = false;
//             calculateBtn.innerHTML = 'Calculate Nutrition';
//         }
//     });

//     function drawChart(data) {
//         const ctx = document.getElementById("nutritionChart").getContext("2d");

//         if (chartInstance) {
//             chartInstance.destroy();
//         }

//         chartInstance = new Chart(ctx, {
//             type: "bar",
//             data: {
//                 labels: ["Protein", "Carbs", "Fat"],
//                 datasets: [{
//                     data: [data.protein, data.carbs, data.fat],
//                     backgroundColor: ["#667eea", "#764ba2", "#f7931e"], // Themed colors
//                     borderRadius: 8
//                 }]
//             },
//             options: {
//                 plugins: {
//                     legend: { display: false }
//                 },
//                 scales: {
//                     x: { ticks: { color: "#2c3e50" } },
//                     y: { ticks: { color: "#2c3e50" } }
//                 }
//             }
//         });
//     }
// });

// // Add spinner CSS if not already in CSS
// document.head.insertAdjacentHTML('beforeend', `
// <style>
// .spinner {
//   display: inline-block;
//   width: 20px;
//   height: 20px;
//   border: 2px solid rgba(255, 255, 255, 0.3);
//   border-radius: 50%;
//   border-top-color: #ffffff;
//   animation: spin 1s ease-in-out infinite;
//   margin-right: 10px;
// }
// @keyframes spin {
//   to { transform: rotate(360deg); }
// }
// </style>
// `);


document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("foodInput");
    const suggestionBox = document.getElementById("suggestions");
    const calculateBtn = document.getElementById("calculateBtn");

    let chartInstance = null;
    let currentIndex = -1; // For keyboard navigation

    // Debounce function to limit API calls
    function debounce(func, delay) {
        let timeout;
        return function (...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    }

    // Debounced input handler for suggestions
    const debouncedInput = debounce(async function () {
        const query = input.value.trim();

        if (query.length < 2) {
            suggestionBox.innerHTML = "";
            suggestionBox.style.display = "none";
            currentIndex = -1;
            return;
        }

        try {
            const response = await fetch("/search_food", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: query })
            });

            if (!response.ok) throw new Error("Failed to fetch suggestions");

            const data = await response.json();
            suggestionBox.innerHTML = "";
            currentIndex = -1;

            data.forEach(function (item, index) {
                const div = document.createElement("div");
                div.innerText = item;
                div.setAttribute("role", "option");
                div.setAttribute("tabindex", "0");
                div.dataset.index = index;

                div.onclick = function () {
                    selectFood(item);
                };

                div.onkeydown = function (e) {
                    if (e.key === "Enter") {
                        selectFood(item);
                        e.preventDefault();
                    }
                };

                suggestionBox.appendChild(div);
            });

            if (data.length > 0) {
                suggestionBox.style.display = "block";
            } else {
                suggestionBox.style.display = "none";
            }
        } catch (error) {
            console.error("Error fetching suggestions:", error);
        }
    }, 300);

    input.addEventListener("input", debouncedInput);

    // Keyboard navigation for suggestions
    input.addEventListener("keydown", function (e) {
        const items = suggestionBox.querySelectorAll("div");
        if (items.length === 0) return;

        if (e.key === "ArrowDown") {
            e.preventDefault();
            currentIndex = (currentIndex + 1) % items.length;
            updateSelection(items);
        } else if (e.key === "ArrowUp") {
            e.preventDefault();
            currentIndex = (currentIndex - 1 + items.length) % items.length;
            updateSelection(items);
        } else if (e.key === "Enter" && currentIndex >= 0) {
            e.preventDefault();
            selectFood(items[currentIndex].innerText);
        } else if (e.key === "Escape") {
            suggestionBox.style.display = "none";
            currentIndex = -1;
        }
    });

    function updateSelection(items) {
        items.forEach((item, index) => {
            if (index === currentIndex) {
                item.classList.add("selected");
                item.focus();
            } else {
                item.classList.remove("selected");
            }
        });
    }

    function selectFood(food) {
        input.value = food;
        suggestionBox.style.display = "none";
        currentIndex = -1;
        input.focus();
    }

    // Hide suggestions on outside click
    document.addEventListener("click", function (e) {
        if (!input.contains(e.target) && !suggestionBox.contains(e.target)) {
            suggestionBox.style.display = "none";
            currentIndex = -1;
        }
    });

    calculateBtn.addEventListener("click", async function () {
        const food = input.value.trim();
        const quantity = document.getElementById("quantityInput").value;

        if (!food || !quantity) {
            alert("Enter food and quantity");
            return;
        }

        // Loading state
        calculateBtn.disabled = true;
        calculateBtn.innerHTML = '<span class="spinner"></span> Calculating...';

        try {
            const response = await fetch("/calculate_nutrition", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    food: food,
                    quantity: quantity
                })
            });

            const data = await response.json();

            if (data.error) {
                alert(data.error);
                return;
            }

            document.getElementById("result").innerHTML = `
                Calories: ${data.calories.toFixed(2)} kcal <br>
                Protein: ${data.protein.toFixed(2)} g <br>
                Carbs: ${data.carbs.toFixed(2)} g <br>
                Fat: ${data.fat.toFixed(2)} g
            `;

            drawChart(data);
        } catch (error) {
            console.error("Error calculating nutrition:", error);
            alert("Failed to calculate nutrition. Please try again.");
        } finally {
            // Reset button
            calculateBtn.disabled = false;
            calculateBtn.innerHTML = 'Calculate Nutrition';
        }
    });

    function drawChart(data) {
        const ctx = document.getElementById("nutritionChart").getContext("2d");

        if (chartInstance) {
            chartInstance.destroy();
        }

        chartInstance = new Chart(ctx, {
            type: "bar",
            data: {
                labels: ["Protein", "Carbs", "Fat"],
                datasets: [{
                    data: [data.protein, data.carbs, data.fat],
                    backgroundColor: ["#667eea", "#764ba2", "#f7931e"], // Themed colors
                    borderRadius: 8
                }]
            },
            options: {
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: { ticks: { color: "#2c3e50" } },
                    y: { ticks: { color: "#2c3e50" } }
                }
            }
        });
    }
});

// Add spinner and selection CSS
document.head.insertAdjacentHTML('beforeend', `
<style>
.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #ffffff;
  animation: spin 1s ease-in-out infinite;
  margin-right: 10px;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
.suggestions .selected {
  background: rgba(102, 126, 234, 0.2);
}
</style>
`);