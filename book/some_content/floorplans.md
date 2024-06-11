<style>
.zoom {
  transition: transform .2s; /* Animation */
  width: 100%;
  height: auto;
  cursor: pointer; /* Set cursor to pointer by default */
  position: relative; /* Required for absolute positioning of magnifier */
}

.zoomed-in {
  transform: scale(1.75); /* Zoom in by 1.75x */
}

.magnifier {
  position: absolute;
  border: 3px solid #000;
  border-radius: 50%;
  cursor: none;
  width: 100px;
  height: 100px;
  overflow: hidden;
  display: none; /* Initially hidden */
  z-index: 10; /* Ensure magnifier is above other elements */
}

.magnifier img {
  position: absolute;
  width: 175%; /* Adjust according to zoom level */
  height: auto;
  transform: scale(2); /* Magnify inside the circle */
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const images = document.querySelectorAll('.zoom');
  
  images.forEach(img => {
    const magnifier = document.createElement('div');
    magnifier.classList.add('magnifier');
    const magnifiedImg = img.cloneNode();
    magnifier.appendChild(magnifiedImg);
    document.body.appendChild(magnifier);

    let clickTimeout;
    
    img.addEventListener('click', () => {
      if (clickTimeout) {
        clearTimeout(clickTimeout);
        clickTimeout = null;
        img.classList.toggle('zoomed-in');
        magnifier.style.display = img.classList.contains('zoomed-in') ? 'block' : 'none';
        if (!img.classList.contains('zoomed-in')) {
          magnifier.style.display = 'none';
        }
      } else {
        clickTimeout = setTimeout(() => {
          clickTimeout = null;
          img.classList.toggle('zoomed-in');
          magnifier.style.display = img.classList.contains('zoomed-in') ? 'block' : 'none';
          if (!img.classList.contains('zoomed-in')) {
            magnifier.style.display = 'none';
          }
        }, 300); // 300ms timeout to detect double-click
      }
    });

    img.addEventListener('mousemove', (e) => {
      if (img.classList.contains('zoomed-in')) {
        let rect = img.getBoundingClientRect();
        let x = e.clientX - rect.left; /* x position within the image */
        let y = e.clientY - rect.top;  /* y position within the image */
        magnifier.style.left = `${e.pageX - magnifier.offsetWidth / 2}px`;
        magnifier.style.top = `${e.pageY - magnifier.offsetHeight / 2}px`;
        magnifiedImg.style.left = `-${x * 2 - magnifier.offsetWidth / 2}px`;
        magnifiedImg.style.top = `-${y * 2 - magnifier.offsetHeight / 2}px`;
      }
    });
    
    img.addEventListener('mouseleave', () => {
      magnifier.style.display = 'none';
    });
    
    img.addEventListener('mouseenter', () => {
      if (img.classList.contains('zoomed-in')) {
        magnifier.style.display = 'block';
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


