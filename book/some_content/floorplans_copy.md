<style>
.zoom {
  transition: transform .2s; /* Animation */
  width: 100%;
  height: auto;
  cursor: pointer; /* Set cursor to pointer by default */
  display: block; /* Center image */
  margin: auto;
}

.zoomed-in {
  transform: scale(1.75); /* Zoom in by 1.75x */
  cursor: url('https://upload.wikimedia.org/wikipedia/commons/0/0b/Magnifying_glass_icon.svg'), auto; /* Change cursor to magnifying glass */
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const images = document.querySelectorAll('.zoom');
  
  images.forEach(img => {
    img.addEventListener('click', () => {
      img.classList.toggle('zoomed-in');
    });
  });
});
</script>

# Floor Plans Copy

In this page you can find the floor plans of the HE Department with the relevant offices in the 2nd and 3rd Floor of the Civil Engineering and Geosciences Building and the Hydraulic Engineering Laboratory.

<div style="text-align: center;">
  <img src="../figures/citg_building.jpg" alt="CITG Building" width="70%">
</div>


**CEG Building 2nd Floor**

<div style="text-align: center;">
  <img src="../figures/floor_plan_second_floor.jpg" class="zoom" alt="Floor Plan Second Floor">
</div>

- [Floor Plan Second Floor (PDF)](../pdfs/2nd_floor.pdf) 
_________________________________________________________________________

**CEG Building 3rd Floor** 

<div style="text-align: center;">
  <img src="../figures/floor_plan_third_floor.jpg" class="zoom" alt="Floor Plan Third Floor">
</div>
  
- [Floor Plan Third Floor (PDF)](../pdfs/3rd_floor.pdf)

_________________________________________________________________________

  
**HE Laboratory**

<div style="text-align: center;">
  <img src="../figures/floor_plan_he_lab.jpg" class="zoom" alt="Floor Plan HE Lab">
</div>

- [HE Lab Floorplan (PDF)](../pdfs/waterlab.pdf)
