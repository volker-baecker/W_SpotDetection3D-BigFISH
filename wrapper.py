import sys
from subprocess import call
from cytomine.models import Job
from biaflows import CLASS_SPTCNT
from biaflows.helpers import BiaflowsJob, prepare_data, upload_data, upload_metrics


def main(argv):
    # 0. Initialize Cytomine client and job if necessary and parse inputs
    with BiaflowsJob.from_cli(argv) as nj:
        problem_cls = CLASS_SPTCNT
        is_2d = False
        nj.job.update(status=Job.RUNNING, progress=0, statusComment="Running workflow for problem class '{}' in {}D".format(problem_cls, 2 if is_2d else 3))

        # 1. Create working directories on the machine
        # 2. Download the images
        nj.job.update(progress=0, statusComment="Initialisation...")
        in_images, gt_images, in_path, gt_path, out_path, tmp_path = prepare_data(problem_cls, nj, is_2d=is_2d, **nj.flags)

        # 3. Call the image analysis workflow using the run script
        nj.job.update(progress=25, statusComment="Launching workflow...")
        command = "/opt/venv/bin/activate && python script.py --in_dir {} --out_dir {} \
                   --radius_xy {} --radius_z {} --threshold {}".format(in_path, out_path, 
                                                                nj.parameters.radius_xy,
                                                                nj.parameters.radius_z,
                                                                nj.parameters.threshold)
        if nj.parameters.detect_threshold:
        	command = command + " --detect_threshold"
        if nj.parameters.remove_duplicates:
        	command = command + " --remove_duplicates"        	
        # Command to test the workflow before it is added to biaflows, which does 
        #   not accept the desciptor.json parameters 
        # command = "python script.py --infld {} --outfld {}".format(in_path, out_path)
        print(command)
        return_code = call(command, shell=True, cwd="/app")  # waits for the subprocess to return

        # 4. Upload the annotation and labels to Cytomine
        upload_data(problem_cls, nj, in_images, out_path, **nj.flags, is_2d=is_2d, monitor_params={
           "start": 60, "end": 90, "period": 0.1
        })

        # 5. Compute and upload the metrics
        nj.job.update(progress=90, statusComment="Computing and uploading metrics...")
        upload_metrics(problem_cls, nj, in_images, gt_path, out_path, tmp_path, **nj.flags)
        
        # 6. End
        nj.job.update(status=Job.TERMINATED, progress=100, statusComment="Finished.")


if __name__ == "__main__":
    main(sys.argv[1:])

