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

# Floor Plans

In this page you can find the floor plans of the HE Department with the relevant offices in the 2nd and 3rd Floor of the Civil Engineering and Geosciences Building and the Hydraulic Engineering Laboratory.

<div style="text-align: center;">
  <img src="../../../_static/figures/tudelft-autumn.jpg" alt="CITG Building" width="70%">
</div>

```{note}
Last update 10-10-2024.
```

### CEG Building 2nd Floor

<div style="text-align: center;">
  <img src="second-floor-october24.jpg" class="zoom" alt="CITG Building">
</div>

- Download pdf of floorplan of second floor [here](second-floor-october2024.pdf). 
_________________________________________________________________________

### CEG Building 3rd Floor

<div style="text-align: center;">
  <img src="third-floor-october2024.jpg" class="zoom" alt="CITG Building">
</div>
  
- Download pdf of floorplan of second floor [here](third-floor-october2024.pdf).

_________________________________________________________________________

  
### HE Laboratory

<div style="text-align: center;">
  <img src="../../../_static/figures/floor_plan_he_lab.jpg" class="zoom" alt="CITG Building" >
</div>

- [HE Lab Floorplan (PDF)](../../../pdfs/waterlab.pdf)
