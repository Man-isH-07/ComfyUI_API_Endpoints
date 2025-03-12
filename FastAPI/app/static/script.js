console.log("Script loaded");

async function fetchPostTypes() {
    try {
        console.log("Fetching post types...");
        const response = await fetch("/post-types");
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        console.log("Post types received:", data);
        const select = document.getElementById("postTypeSelect");
        data.post_types.forEach(type => {
            const option = document.createElement("option");
            option.value = type;
            option.text = type;
            select.appendChild(option);
        });
    } catch (error) {
        console.error("Error fetching post types:", error);
    }
}

async function loadNews() {
    const category = document.getElementById("categorySelect").value;
    const newsSelect = document.getElementById("newsSelect");
    try {
        const response = await fetch(`/trends?category=${category}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        console.log("News received:", data);
        newsSelect.innerHTML = '<option value="">-- Select News --</option>';
        data.articles.forEach(article => {
            const option = document.createElement("option");
            option.value = article.title;
            option.text = article.title;
            newsSelect.appendChild(option);
        });
        updateTrend(); 
    } catch (error) {
        console.error("Error loading news:", error);
        newsSelect.innerHTML = '<option value="">Error loading news</option>';
    }
}

async function loadForm() {
    const postType = document.getElementById("postTypeSelect").value;
    const formFieldsDiv = document.getElementById("formFields");
    const generateBtn = document.getElementById("generateBtn");
    const updateTrendsBtn = document.getElementById("updateTrendsBtn");
    formFieldsDiv.innerHTML = "";
    generateBtn.disabled = true;
    updateTrendsBtn.style.display = "inline-block";

    if (!postType) return;

    try {
        const response = await fetch(`/generate_prompt_form?post_type=${postType}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        console.log("Form data received:", data); // Debug log

        const fields = [...data.required_fields, ...data.optional_fields];
        fields.forEach(field => {
            const div = document.createElement("div");
            div.className = "input-group";
            const label = document.createElement("label");
            label.textContent = `${field} ${data.required_fields.includes(field) ? '*' : ''}:`;
            label.htmlFor = field;
            div.appendChild(label);

            if (field === "trend") {
                const input = document.createElement("input");
                input.type = "hidden";
                input.id = field;
                input.name = field;
                input.value = document.getElementById("newsSelect").value || "";
                div.appendChild(input);
                const span = document.createElement("span");
                span.id = "trendDisplay";
                span.textContent = document.getElementById("newsSelect").value || "Select a news item above";
                div.appendChild(span);
            } else {
                const input = document.createElement("input");
                input.type = "text";
                input.id = field;
                input.name = field;
                input.placeholder = data.example[field] || `Enter ${field}`; 
                div.appendChild(input);
            }
            formFieldsDiv.appendChild(div);
        });

        const newsSelectValue = document.getElementById("newsSelect").value;
        generateBtn.disabled = !newsSelectValue && data.required_fields.includes("trend");
    } catch (error) {
        console.error("Error loading form:", error);
    }
}

async function updateTrends() {
    const category = document.getElementById("categorySelect").value;
    try {
        const response = await fetch(`/update_trends?category=${category}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        console.log("Trends updated");
        loadNews();
        const generateBtn = document.getElementById("generateBtn");
        const newsSelectValue = document.getElementById("newsSelect").value;
        generateBtn.disabled = !newsSelectValue;
    } catch (error) {
        console.error("Error updating trends:", error);
    }
}

function updateTrend() {
    const newsSelect = document.getElementById("newsSelect");
    const trendInput = document.getElementById("trend");
    const trendDisplay = document.getElementById("trendDisplay");
    if (trendInput && trendDisplay) {
        trendInput.value = newsSelect.value;
        trendDisplay.textContent = newsSelect.value || "Select a news item above";
        console.log("Trend updated to:", trendInput.value);
        // Update Generate button state
        const generateBtn = document.getElementById("generateBtn");
        generateBtn.disabled = !newsSelect.value;
    }
}
async function generatePrompt() {
    const postType = document.getElementById("postTypeSelect").value;
    const payload = { post_type: postType };
    
    updateTrend();
    
    const fields = document.querySelectorAll("#formFields input");
    fields.forEach(field => {
        if (field.value) {
            payload[field.id] = field.value;
        }
    });
    console.log("Payload sent:", payload); 

    try {
        const response = await fetch("/generate_prompt", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const result = await response.json();
        document.getElementById("result").textContent = result.generated_prompt || "Error generating prompt";
    } catch (error) {
        console.error("Error generating prompt:", error);
        document.getElementById("result").textContent = "Error generating prompt: " + error.message;
    }
}

document.getElementById("newsSelect").addEventListener("change", updateTrend);

fetchPostTypes();
loadNews(); 