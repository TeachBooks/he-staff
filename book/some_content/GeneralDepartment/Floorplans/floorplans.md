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
  <img src="../../../figures/citg_building.jpg" alt="CITG Building" width="70%">
</div>


### CEG Building 2nd Floor

- Download image of floorplan of second floor [here](./Appendices/second-floor-nov-24.jpg).
- Download pdf of floorplan of second floor [here](./Appendices/second-floor-nov-24.pdf).
```{note}
Last update 19-12-2024.
```
_________________________________________________________________________

### CEG Building 3rd Floor

```{note}
You can preview the files by right clicking on the links below and selecting open in new tab, for both jpg and pdf files.
```

- Download image of floorplan of third floor [here](./Appendices/third-floor-dec-24.jpg).

```{note}
Last update 19-12-2024.
```
_________________________________________________________________________

  
### HE Laboratory

- Download image of floorplan of waterlab [here](./Appendices/wlab_nov_24.jpg).
- Download pdf of floorplan of waterlab [here](./Appendices/wlab_nov_24.pdf).

