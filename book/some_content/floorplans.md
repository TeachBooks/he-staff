<style>
.zoom {
  transition: transform .2s; /* Animation */
  width: 100%;
  height: auto;
}

.zoomed-in {
  transform: scale(3); /* Zoom in by 3x */
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const images = document.querySelectorAll('.zoom');
  images.forEach(img => {
    let clickTimeout;
    img.addEventListener('click', () => {
      if (clickTimeout) {
        clearTimeout(clickTimeout);
        clickTimeout = null;
        img.classList.toggle('zoomed-in');
      } else {
        clickTimeout = setTimeout(() => {
          clickTimeout = null;
        }, 300); // 300ms timeout to detect double-click
      }
    });
  });
});
</script>

# Floor Plans

In this page you can find the floor plans of the HE Department with the relevant offices in the 2nd and 3rd Floor of the Civil Engineering and Geosciences Building and the Hydraulic Engineering Laboratory.

![CiTG Building](../figures/citg_building.jpg)

_________________________________________________________________________


**CEG Building 2nd Floor**

<img src="../figures/floor-plan_second_floor.jpg" alt="Floor Plan Second Floor" width="800"/>

- [Floor Plan Second Floor (PDF)](../pdfs/2nd_floor.pdf) 
_________________________________________________________________________

**CEG Building 3rd Floor** 

  <img src="../figures/floor-plan_third_floor.jpg" alt="Floor Plan Third Floor" width="1000" class="zoom"/>
  
- [Floor Plan Third Floor (PDF)](../pdfs/3rd_floor.pdf)

_________________________________________________________________________

  
**HE Laboratory**

<img src="../figures/floor-plan_he-lab.jpg" alt="HE Lab" width="800"/>

- [HE Lab Floorplan (PDF)](../pdfs/waterlab.pdf)


