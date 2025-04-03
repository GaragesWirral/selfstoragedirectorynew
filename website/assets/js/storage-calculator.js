/**
 * Storage Size Calculator
 * Simple script to calculate recommended storage size based on user selections
 */

function calculateStorageSize() {
    // Get values from form
    const boxes = document.getElementById('calc-boxes').value;
    const furniture = document.getElementById('calc-furniture').value;
    const appliances = document.getElementById('calc-appliances').value;
    const electronics = document.getElementById('calc-electronics').value;
    
    // Base calculation
    let totalSqFt = 0;
    
    // Add space for boxes
    switch(boxes) {
        case 'none':
            totalSqFt += 0;
            break;
        case 'few':
            totalSqFt += 10;
            break;
        case 'several':
            totalSqFt += 25;
            break;
        case 'many':
            totalSqFt += 40;
            break;
    }
    
    // Add space for furniture
    switch(furniture) {
        case 'none':
            totalSqFt += 0;
            break;
        case 'small':
            totalSqFt += 25;
            break;
        case 'medium':
            totalSqFt += 50;
            break;
        case 'large':
            totalSqFt += 100;
            break;
    }
    
    // Add space for appliances
    switch(appliances) {
        case 'none':
            totalSqFt += 0;
            break;
        case 'small':
            totalSqFt += 15;
            break;
        case 'large':
            totalSqFt += 40;
            break;
    }
    
    // Add space for electronics
    switch(electronics) {
        case 'none':
            totalSqFt += 0;
            break;
        case 'some':
            totalSqFt += 15;
            break;
        case 'many':
            totalSqFt += 30;
            break;
    }
    
    // Determine recommended unit size
    let recommendation = "";
    if (totalSqFt <= 25) {
        recommendation = "25 sq ft - Ideal for small number of boxes and small items";
    } else if (totalSqFt <= 50) {
        recommendation = "50 sq ft - Ideal for contents of a small flat";
    } else if (totalSqFt <= 75) {
        recommendation = "75 sq ft - Ideal for contents of a 1-bedroom flat";
    } else if (totalSqFt <= 100) {
        recommendation = "100 sq ft - Ideal for contents of a 2-bedroom flat";
    } else if (totalSqFt <= 150) {
        recommendation = "150 sq ft - Ideal for contents of a small house";
    } else if (totalSqFt <= 200) {
        recommendation = "200 sq ft - Ideal for contents of a 3-bedroom house";
    } else {
        recommendation = "250+ sq ft - Consider our larger units for entire house contents";
    }
    
    // Display the result
    document.getElementById('calculator-result').innerHTML = `
        <div class="result-box">
            <h3>Recommended Size:</h3>
            <p>${recommendation}</p>
        </div>
    `;
    
    // Make the result visible
    document.getElementById('calculator-result').style.display = 'block';
    
    // Smooth scroll to results
    document.getElementById('calculator-result').scrollIntoView({behavior: 'smooth'});
    
    return false; // Prevent form submission
} 