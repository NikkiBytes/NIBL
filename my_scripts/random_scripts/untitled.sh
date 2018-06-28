read -p "Enter unique dicom path: " dicom_path
source=${f}
if echo "$dicom_path" | grep -q "$source"; then
echo "matched";

else
echo "no match";
fi

MAIN="/test"
INPUT="Raw_Data/test/bevel"
CONVERT="bevel_converter.py"
OUT="Experiments/test"
