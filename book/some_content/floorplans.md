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

![CiTG Building](../figures/citg_building.jpg)


**Note**: You have the option to download the figure as a PDF or image file, or alternatively, open it in a new tab for a larger view.
_________________________________________________________________________


**CEG Building 2nd Floor**

![Floor Plan Second Floor](../figures/floor-plan_second_floor.jpg)

- [Floor Plan Second Floor (PDF)](../pdfs/2nd_floor.pdf) 
_________________________________________________________________________

**CEG Building 3rd Floor** 

![Floor Plan Third Floor](../figures/floor-plan_third_floor.jpg)
  
- [Floor Plan Third Floor (PDF)](../pdfs/3rd_floor.pdf)

_________________________________________________________________________

  
**HE Laboratory**

![HE Lab Floorplan](../figures/floor-plan_he-lab.jpg)

- [HE Lab Floorplan (PDF)](../pdfs/waterlab.pdf)




