import cv2
import os

def process_images(image_paths, output_folder="Photos", size=(512, 512)):
    # Create the output folder if it doesn't exist.
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Go through each image
    for image_path in image_paths:
        if not os.path.exists(image_path):
            print(f"Warning: {image_path} does not exist.")
            continue
        
        # Read the image.
        img = cv2.imread(image_path)
        # cv2.imshow("img", img)
        if img is None:
            print(f"Error loading image: {image_path}")
            continue
        
        # Convert the image to grayscale.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("gray", gray)

        # Resize the grayscale image.
        resized = cv2.resize(gray, size)
        # cv2.imshow("resized", resized)
        
        # Normalize the pixel values to the range [0, 1].
        normalized = resized.astype("float32") / 255.0
        # cv2.imshow("normalized", normalized)
        
        # For saving, scale normalized values back to [0, 255].
        visual_image = (normalized * 255).astype("uint8")
        # cv2.imshow("visual_image", visual_image)

        # Construct output filename.
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_path = os.path.join(output_folder, f"processed_{base_name}.jpg")
        
        # Save the processed image.
        cv2.imwrite(output_path, visual_image)
        print(f"Saved processed image: {output_path}")

images = [
    r"OpevCV_prat\playing-cards-master\img\cards-[C0]-001.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[C0]-002.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[C0]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C2]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C2]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C2]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C3]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C3]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C3]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C4]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C4]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C4]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C5]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C5]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C5]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C6]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C6]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C6]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C7]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C7]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C7]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C8]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C8]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C8]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C9]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C9]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[C9]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CA]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CA]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CA]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CJ]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CJ]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CJ]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CK]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CK]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CK]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CQ]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CQ]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[CQ]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D0]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D0]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D0]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D2]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D2]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D2]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D3]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D3]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D3]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D4]-001.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[D4]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D4]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D5]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D5]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D5]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D6]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D6]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D6]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D7]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D7]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D7]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D8]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D8]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D8]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D9]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D9]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[D9]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DA]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DA]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DA]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DJ]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DJ]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DJ]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DK]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DK]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DK]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DQ]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DQ]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[DQ]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H0]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H0]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H0]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H2]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H2]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H2]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H3]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H3]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H3]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H4]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H4]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H4]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H5]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H5]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H5]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H6]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H6]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H6]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H7]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H7]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H7]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H8]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H8]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H8]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H9]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H9]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[H9]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HA]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HA]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HA]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HJ]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HJ]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HJ]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HK]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HK]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HK]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HQ]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HQ]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[HQ]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S0]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S0]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S0]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S2]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S2]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S2]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S3]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S3]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S3]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S4]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S4]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S4]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S5]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S5]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S5]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S6]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S6]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S6]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S7]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S7]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S7]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S8]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S8]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S8]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S9]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S9]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[S9]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SA]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SA]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SA]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SJ]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SJ]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SJ]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SK]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SK]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SK]-004.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SQ]-001.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SQ]-002.jpg",
    r"OpevCV_prat\playing-cards-master\img\cards-[SQ]-004.jpg"]
immg = [r"OpevCV_prat\playing-cards-master\img\cards-[C4]-003.jpg"]
imgg = [
    r"OpevCV_prat\playing-cards-master\img\cards-[C0]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[C2]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[C3]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[C4]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[C5]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[C6]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[C7]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[C8]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[C9]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[CA]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[CJ]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[CK]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[CQ]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[D0]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[D2]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[D3]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[D4]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[D5]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[D6]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[D7]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[D8]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[D9]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[DA]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[DJ]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[DK]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[DQ]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[H0]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[H2]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[H3]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[H4]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[H5]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[H6]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[H7]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[H8]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[H9]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[HA]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[HJ]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[HK]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[HQ]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[S0]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[S2]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[S3]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[S4]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[S5]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[S6]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[S7]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[S8]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[S9]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[SA]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[SJ]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[SK]-003.jpg", 
    r"OpevCV_prat\playing-cards-master\img\cards-[SQ]-003.jpg", ]
process_images(imgg)

cv2.waitKey(0) # holds the windows in plase for some reason.
cv2.destroyAllWindows() # read the name
