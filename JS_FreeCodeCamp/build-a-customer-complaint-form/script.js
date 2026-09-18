const fullName = document.getElementById("full-name");
const email = document.getElementById("email");
const orderNo = document.getElementById("order-no");
const productCode = document.getElementById("product-code");
const quantity = document.getElementById("quantity");

const complaintsGroup = document.getElementById("complaints-group");
const complaints = complaintsGroup.querySelectorAll("input[type='checkbox']");
const otherComplaint = document.getElementById("other-complaint");
const complaintDescription = document.getElementById("complaint-description");

const solutionsGroup = document.getElementById("solutions-group");
const solutions = solutionsGroup.querySelectorAll("input[type='radio']");
const otherSolution = document.getElementById("other-solution");
const solutionDescription = document.getElementById("solution-description");

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const orderRegex = /^2024\d{6}$/;
const productRegex = /^[A-Za-z]{2}\d{2}-[A-Za-z]\d{3}-[A-Za-z]{2}\d$/;

function setBorder(element, valid) {
  if (valid === true) {
    element.style.borderColor = "green";
  } else {
    element.style.borderColor = "red";
  }
}

function validateForm() {
  const result = {};
  if (fullName.value.trim() !== "") {
    result["full-name"] = true;
  } else {
    result["full-name"] = false;
  }

  if (emailRegex.test(email.value)) {
    result["email"] = true;
  } else {
    result["email"] = false;
  }

  if (orderRegex.test(orderNo.value)) {
    result["order-no"] = true;
  } else {
    result["order-no"] = false;
  }

  if (productRegex.test(productCode.value)) {
    result["product-code"] = true;
  } else {
    result["product-code"] = false;
  }

  const q = Number(quantity.value);

  if (Number.isInteger(q) && q > 0) {
    result["quantity"] = true;
  } else {
    result["quantity"] = false;
  }

  let complaintChecked = false;

  for (let i = 0; i < complaints.length; i++) {
    if (complaints[i].checked) {
      complaintChecked = true;
    }
  }

  result["complaints-group"] = complaintChecked;

  if (otherComplaint.checked) {
    if (complaintDescription.value.trim().length >= 20) {
      result["complaint-description"] = true;
    } else {
      result["complaint-description"] = false;
    }
  } else {
    result["complaint-description"] = true;
  }

  let solutionChecked = false;

  for (let i = 0; i < solutions.length; i++) {
    if (solutions[i].checked) {
      solutionChecked = true;
    }
  }

  result["solutions-group"] = solutionChecked;

  if (otherSolution.checked) {
    if (solutionDescription.value.trim().length >= 20) {
      result["solution-description"] = true;
    } else {
      result["solution-description"] = false;
    }
  } else {
    result["solution-description"] = true;
  }
  return result;
}

function isValid(obj) {
  for (const key in obj) {
    if (obj[key] !== true) {
      return false;
    }
  }
  return true;
}

fullName.addEventListener("change", function() {
  let valid;
  if (fullName.value.trim() !== "") {
    valid = true;
  } else {
    valid = false;
  }
  setBorder(fullName, valid);
});

email.addEventListener("change", function() {
  let valid;
  if (emailRegex.test(email.value)) {
    valid = true;
  } else {
    valid = false;
  }
  setBorder(email, valid);
});

orderNo.addEventListener("change", function() {
  let valid;
  if (orderRegex.test(orderNo.value)) {
    valid = true;
  } else {
    valid = false;
  }
  setBorder(orderNo, valid);
});

productCode.addEventListener("change", function() {
  let valid;
  if (productRegex.test(productCode.value)) {
    valid = true;
  } else {
    valid = false;
  }
  setBorder(productCode, valid);
});

quantity.addEventListener("change", function() {
  const q = Number(quantity.value);
  let valid;
  if (Number.isInteger(q) && q > 0) {
    valid = true;
  } else {
    valid = false;
  }
  setBorder(quantity, valid);
});

for (let i = 0; i < complaints.length; i++) {
  complaints[i].addEventListener("change", function() {
    let valid = false;
    for (let j = 0; j < complaints.length; j++) {
      if (complaints[j].checked) {
        valid = true;
      }
    }
    setBorder(complaintsGroup, valid);
  });
}

complaintDescription.addEventListener("change", function() {
  if (otherComplaint.checked) {
    let valid;
    if (complaintDescription.value.trim().length >= 20) {
      valid = true;
    } else {
      valid = false;
    }
    setBorder(complaintDescription, valid);
  }
});

for (let i = 0; i < solutions.length; i++) {
  solutions[i].addEventListener("change", function() {
    let valid = false;
    for (let j = 0; j < solutions.length; j++) {
      if (solutions[j].checked) {
        valid = true;
      }
    }
    setBorder(solutionsGroup, valid);
  });
}

solutionDescription.addEventListener("change", function() {
  if (otherSolution.checked) {
    let valid;
    if (solutionDescription.value.trim().length >= 20) {
      valid = true;
    } else {
      valid = false;
    }
    setBorder(solutionDescription, valid);
  }
});

form.addEventListener("submit", function(e) {
  const validation = validateForm();
  if (!isValid(validation)) {
    e.preventDefault();
    if (!validation["full-name"]) setBorder(fullName, false);
    if (!validation["email"]) setBorder(email, false);
    if (!validation["order-no"]) setBorder(orderNo, false);
    if (!validation["product-code"]) setBorder(productCode, false);
    if (!validation["quantity"]) setBorder(quantity, false);
    if (!validation["complaints-group"]) setBorder(complaintsGroup, false);
    if (!validation["complaint-description"]) setBorder(complaintDescription, false);
    if (!validation["solutions-group"]) setBorder(solutionsGroup, false);
    if (!validation["solution-description"]) setBorder(solutionDescription, false);
  }
});