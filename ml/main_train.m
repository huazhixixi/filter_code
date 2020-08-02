net_anc_target = train_ann(feature,anc_target);
net_anc_target2 = train_ann(feature,anc_target2);
net_pnc_target = train_ann(feature,pnc_target);
% net_pnc_target2 = train_ann(feature,pnc_target2);
fase1 = featuretargetfalseancpnctarget(:,1:end-1);
error1 = net_anc_target(feature');
error2 = net_anc_target2(feature');
error3 = net_pnc_target(feature');

fase1(:,1) = fase1(:,1)-error1';

fase1(:,2) = fase1(:,2)-error2';

fase1(:,3) = fase1(:,3)-error3';