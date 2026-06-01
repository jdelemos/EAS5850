import io
import json

import pyorthanc


def _series_number(series):
    val = series.get_main_information()["MainDicomTags"].get("SeriesNumber") or 0
    return int(val)


def _instance_number(instance):
    val = instance.get_main_information()["MainDicomTags"].get("InstanceNumber") or 0
    return int(val)


def part2_investigate(client):
    patients = pyorthanc.find_patients(
        client=client, query={"PatientID": "A034518"}
    )
    patient = patients[0]
    study = patient.studies[0]

    series_sorted = sorted(study.series, key=_series_number)
    target_series = next(
        (s for s in series_sorted if _series_number(s) == 4),
        series_sorted[3],
    )

    instances_sorted = sorted(target_series.instances, key=_instance_number)
    target_instance = next(
        (i for i in instances_sorted if _instance_number(i) == 130),
        instances_sorted[129],
    )

    ds = target_instance.get_pydicom()
    pixels = ds.pixel_array

    result = {
        "Age": str(getattr(ds, "PatientAge", "")),
        "Sex": str(getattr(ds, "PatientSex", "")),
        "StudyDescription": str(getattr(ds, "StudyDescription", "")),
        "Modality": str(getattr(ds, "Modality", "")),
        "Manufacturer": str(getattr(ds, "Manufacturer", "")),
        "PatientID": str(getattr(ds, "PatientID", "")),
        "NumSeries": len(study.series),
        "StudyInstanceUID": str(getattr(ds, "StudyInstanceUID", "")),
        "NumRows": int(ds.Rows),
        "NumCols": int(ds.Columns),
        "MinPixelVal": float(pixels.min()),
        "MaxPixelVal": float(pixels.max()),
        "MeanPixelVal": float(pixels.mean()),
    }

    with open("study_info.json", "w") as f:
        json.dump(result, f, indent=2)


def part3_modify(client):
    patients = pyorthanc.find_patients(
        client=client, query={"PatientID": "3142537564"}
    )
    if not patients:
        print("No patient found with ID 3142537564")
        return
    patient = patients[0]
    study = patient.studies[0]
    original_study_id = study.id_

    for series in study.series:
        for instance in series.instances:
            ds = instance.get_pydicom()
            ds.StudyInstanceUID = "1.2.840.20252025"
            ds.AccessionNumber = "EAS5850-12345678"
            ds.PatientBirthDate = "19780101"
            ds.PatientSex = "O"
            ds.StudyDate = "20221231"
            ds.PatientID = "8675309"
            ds.ReferringPhysicianName = "Spock^Thomas"

            buf = io.BytesIO()
            ds.save_as(buf, enforce_file_format=True)
            client.post_instances(buf.getvalue())

    client.delete_studies_id(original_study_id)


def main():
    client = pyorthanc.Orthanc("http://localhost:8042")
    part2_investigate(client)
    part3_modify(client)


if __name__ == "__main__":
    main()
