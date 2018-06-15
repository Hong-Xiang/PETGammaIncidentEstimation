for i in {1..6}
do
python ../src/dataset/discrete/generate.py -c compton_data_2/$i/true_scatter_randomM.csv -h compton_data_2/$i/hitsM.csv -t gamma3.db &
done
