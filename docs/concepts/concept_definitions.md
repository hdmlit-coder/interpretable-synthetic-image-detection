# Operational Definitions for the Phase 2 Pilot

## Annotation Scale

- `0`: no visible inconsistency
- `1`: weak or uncertain inconsistency
- `2`: clear inconsistency
- `3`: severe and obvious inconsistency
- `N/A`: the concept cannot be evaluated in the image

`0` and `N/A` are different.

- Use `0` when the relevant content is visible and appears normal.
- Use `N/A` when the relevant content is absent or cannot be inspected.

---

## 1. Hand Anatomy

### Definition

The degree to which visible hands contain anatomically unusual or implausible structures.

### Include

- incorrect number of fingers,
- fused fingers,
- disconnected fingers,
- malformed palms,
- implausible joints,
- impossible finger orientation.

### Exclude

- motion blur,
- gloves,
- hands partly outside the frame,
- occlusion,
- unusual but physically possible poses.

### Applicability

Use `N/A` when no hand can be inspected.

---

## 2. Facial Consistency

### Definition

The degree to which visible facial components are geometrically and visually coherent.

### Include

- misplaced eyes,
- distorted teeth,
- asymmetric facial parts,
- blended ears,
- malformed facial geometry,
- inconsistent skin regions.

### Exclude

- normal facial asymmetry,
- expression,
- makeup,
- occlusion,
- intentional artistic style.

### Applicability

Use `N/A` when no face can be inspected.

---

## 3. Text Readability

### Definition

The degree to which visible text contains malformed, meaningless, incomplete, or inconsistent characters.

### Include

- nonsense words,
- merged letters,
- broken characters,
- impossible spelling,
- inconsistent symbols,
- unreadable signs intended to contain text.

### Exclude

- text that is too small,
- unfamiliar but valid languages,
- decorative symbols,
- intentionally blurred text.

### Applicability

Use `N/A` when no text is visible.

---

## 4. Repeated Texture Patterns

### Definition

The presence of duplicated or unnaturally repeated local visual patterns.

### Include

- duplicated leaves,
- repeated facial details,
- copied background patches,
- suspiciously similar windows,
- unnatural recurring texture elements.

### Exclude

- brick walls,
- fences,
- fabric patterns,
- tiled floors,
- naturally repeated architecture.

### Applicability

This concept can usually be evaluated in all images.

---

## 5. Object Boundary Consistency

### Definition

The degree to which object edges are visually coherent and properly separated from surrounding regions.

### Include

- objects merging into each other,
- disappearing edges,
- irregular outlines,
- incomplete object contours,
- objects blending unnaturally into the background.

### Exclude

- depth-of-field blur,
- motion blur,
- transparent materials,
- shadows,
- soft materials such as fur.

### Applicability

This concept can usually be evaluated in all images.

---

## 6. Background Coherence

### Definition

The degree to which the background forms a visually and semantically coherent scene.

### Include

- malformed architecture,
- merged background objects,
- incomplete structures,
- incoherent repeated elements,
- impossible spatial relationships.

### Exclude

- intentional blur,
- abstract backgrounds,
- surreal artwork,
- shallow depth of field.

### Applicability

Use 'N/A' only when no meaningful background is visible.
