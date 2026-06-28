export function getTagClass(value: string): string {
  switch (value) {
    case "Boys":
    case "Tiffin":
      return "tag-indigo";
    case "Girls":
    case "Dhaba":
      return "tag-rose";
    case "Co-ed":
    case "Bhojnalaya":
      return "tag-olive";
    default:
      return "tag-indigo";
  }
}
